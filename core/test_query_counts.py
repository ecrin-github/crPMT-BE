from types import SimpleNamespace

from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APITestCase

from context.models.country import Country
from context.models.ctu import CTU
from context.models.hospital import Hospital
from context.models.organisation import Organisation
from context.models.person import Person
from core.models.centre import Centre
from core.models.ctu_agreement import CTUAgreement
from core.models.ctu_agreement_amendment import CTUAgreementAmendment
from core.models.notification import Notification
from core.models.project import Project
from core.models.reporting_period import ReportingPeriod
from core.models.safety_notification import SafetyNotification
from core.models.satisfaction_survey import SatisfactionSurvey
from core.models.study import Study
from core.models.study_agreement import StudyAgreement
from core.models.study_agreement_amendment import StudyAgreementAmendment
from core.models.study_country import StudyCountry
from core.models.study_ctu import StudyCTU
from core.models.submission import Submission
from core.models.visit import Visit


class QueryCountTests(APITestCase):
    """
    Number of SQL queries of the endpoints used when saving and reloading a study (#125).
    The nested output serializers used to make one query per related object (496 queries for the study below).
    """

    @classmethod
    def setUpTestData(cls):
        cls.fr = Country.objects.create(iso2="FR", iso3="FRA", name="France")
        cls.de = Country.objects.create(iso2="DE", iso3="DEU", name="Germany")
        cls.it = Country.objects.create(iso2="IT", iso3="ITA", name="Italy")
        cls.org = Organisation.objects.create(name="Org", country=cls.fr)
        cls.person = Person.objects.create(full_name="Person", country=cls.fr)
        cls.ctus = [CTU.objects.create(name=f"CTU {i}", country=cls.fr) for i in range(2)]
        cls.hospitals = [Hospital.objects.create(name=f"Hospital {i}", country=cls.fr) for i in range(2)]

        cls.project = cls.create_project()
        cls.study = cls.create_study(cls.project)
        cls.study_countries = [cls.create_study_country(cls.study, country) for country in (cls.fr, cls.de)]

    @classmethod
    def create_project(cls):
        project = Project.objects.create(name="Project", coordinator=cls.person, coordinating_institution=cls.org)
        ReportingPeriod.objects.bulk_create([ReportingPeriod(project=project, stage=i) for i in range(2)])
        return project

    @classmethod
    def create_study(cls, project):
        study = Study.objects.create(
            short_title="Study", project=project, sponsor_organisation=cls.org, sponsor_country=cls.fr,
            lead_ctu=cls.ctus[0], coordinating_investigator=cls.person, c_euco=cls.person, coordinating_country=cls.fr,
        )
        study_agreement = StudyAgreement.objects.create(study=study)
        StudyAgreementAmendment.objects.bulk_create(
            [StudyAgreementAmendment(study_agreement=study_agreement) for _ in range(2)])
        SatisfactionSurvey.objects.bulk_create([SatisfactionSurvey(study=study) for _ in range(2)])
        return study

    @classmethod
    def create_study_country(cls, study, country):
        """Study country with 2 study CTUs, 4 centres, 12 visits, submissions, notifications and agreements"""
        sc = StudyCountry.objects.create(study=study, country=country)
        Submission.objects.bulk_create([Submission(study_country=sc) for _ in range(3)])
        Notification.objects.bulk_create([Notification(study_country=sc) for _ in range(2)])
        sc.safety_notifications.set([SafetyNotification.objects.create() for _ in range(2)])

        for ctu in cls.ctus:
            sctu = StudyCTU.objects.create(study=study, study_country=sc, ctu=ctu, contact_person=cls.person)
            ctu_agreement = CTUAgreement.objects.create(study_ctu=sctu)
            CTUAgreementAmendment.objects.bulk_create(
                [CTUAgreementAmendment(ctu_agreement=ctu_agreement) for _ in range(2)])
            for hospital in cls.hospitals:
                centre = Centre.objects.create(study_ctu=sctu, hospital=hospital, pi=cls.person)
                Visit.objects.bulk_create([Visit(centre=centre) for _ in range(3)])
        return sc

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=SimpleNamespace(is_authenticated=True))

    def count_queries(self, method, url, data=None):
        with CaptureQueriesContext(connection) as context:
            response = getattr(self.client, method)(url, data, format="json")
        self.assertLess(response.status_code, 300, getattr(response, "data", None))
        return len(context.captured_queries)

    def assert_constant_queries(self, url, add_data, max_queries):
        """The number of queries must not grow with the amount of nested data"""
        before = self.count_queries("get", url)
        add_data()
        after = self.count_queries("get", url)

        self.assertEqual(before, after, "The number of queries grows with the nested data (N+1)")
        self.assertLessEqual(before, max_queries)

    def test_study_detail(self):
        self.assert_constant_queries(
            f"/api/core/studies/{self.study.id}",
            lambda: self.create_study_country(self.study, self.it),
            max_queries=24,
        )

    def test_project_detail(self):
        self.assert_constant_queries(
            f"/api/core/projects/{self.project.id}",
            lambda: self.create_study_country(self.create_study(self.project), self.it),
            max_queries=22,
        )

    def test_project_list(self):
        def add_project():
            study = self.create_study(self.create_project())
            self.create_study_country(study, self.it)

        self.assert_constant_queries("/api/core/projects", add_project, max_queries=7)

    def test_bulk_update_responses(self):
        # Each item is still validated and saved separately, but the nested objects of the response are loaded at once
        sc = self.study_countries[0]
        sctu = sc.study_ctus.first()
        cases = [
            ("notifications", [{"id": n.id, "study_country": sc.id} for n in sc.notifications.all()], 10),
            ("submissions", [{"id": s.id, "study_country": sc.id} for s in sc.submissions.all()], 12),
            ("ctu-agreement-amendments",
             [{"id": a.id, "ctu_agreement": a.ctu_agreement_id}
              for a in CTUAgreementAmendment.objects.filter(ctu_agreement__study_ctu=sctu)], 8),
            ("study-agreement-amendments",
             [{"id": a.id, "study_agreement": a.study_agreement_id}
              for a in StudyAgreementAmendment.objects.filter(study_agreement__study=self.study)], 8),
        ]
        for prefix, payload, max_queries in cases:
            with self.subTest(prefix=prefix):
                self.assertLessEqual(
                    self.count_queries("put", f"/api/core/{prefix}/bulk_update", payload), max_queries)
