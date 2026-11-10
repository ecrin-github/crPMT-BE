from datetime import date, datetime, time, timedelta
from types import SimpleNamespace

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from rest_framework.test import APITestCase

from context.models.authority import Authority
from context.models.country import Country
from context.models.ctu import CTU
from context.models.hospital import Hospital
from context.models.visit_type import VisitType
from core.models.centre import Centre
from core.models.project import Project
from core.models.reporting_period import ReportingPeriod
from core.models.study import Study
from core.models.study_country import StudyCountry
from core.models.study_ctu import StudyCTU
from core.models.submission import Submission
from core.models.visit import Visit
from core.views.dashboard import DEADLINES_DAYS, DEADLINES_LIMIT, SUBMISSIONS_MONTHS, DashboardView

URL = "/api/core/dashboard"


def days_from_today(days):
    """Aware datetime at noon, `days` days from today (negative: in the past)"""
    return timezone.make_aware(datetime.combine(timezone.localdate() + timedelta(days=days), time(12)))


class DashboardTests(APITestCase):
    """Dashboard data of the internal main page (#36)"""

    @classmethod
    def setUpTestData(cls):
        cls.fr = Country.objects.create(iso2="FR", iso3="FRA", name="France")
        cls.ctu = CTU.objects.create(name="CTU", country=cls.fr)
        cls.hospital = Hospital.objects.create(name="Hospital", country=cls.fr)
        cls.visit_type = VisitType.objects.create(code="SIV", name="Site initiation visit")
        cls.project = Project.objects.create(short_name="Project A")

    def setUp(self):
        self.client.force_authenticate(user=SimpleNamespace(is_authenticated=True))

    def get_dashboard(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def create_centre(self, short_title="Study A"):
        study = Study.objects.create(short_title=short_title, project=self.project)
        sc = StudyCountry.objects.create(study=study, country=self.fr)
        sctu = StudyCTU.objects.create(study=study, study_country=sc, ctu=self.ctu)
        return sc, Centre.objects.create(study_ctu=sctu, hospital=self.hospital)

    # ---- Studies by status ----

    def test_studies_by_status(self):
        for status in ["Start-up phase", "Running phase: Follow up", "Running phase: Organisation of close-out",
                       "Completed", "On hold", "Old renamed status", None, ""]:
            Study.objects.create(status=status)

        counts = {item["name"]: item["value"] for item in self.get_dashboard()["studiesByStatus"]}

        self.assertEqual(counts, {
            "Start-up": 1, "Running": 2, "Completion": 0, "Completed": 1, "Stopped": 1, "Other": 1, "Not set": 2,
        })

    # ---- Regulatory submissions ----

    def test_submissions_by_month(self):
        sc, _ = self.create_centre()
        last_month, this_month = DashboardView.get_last_months(2)   # Oldest first
        in_this_month = timezone.make_aware(datetime.combine(this_month, time(12)))
        in_last_month = timezone.make_aware(datetime.combine(last_month, time(12)))
        too_old = in_last_month - timedelta(days=31 * SUBMISSIONS_MONTHS)

        Submission.objects.create(study_country=sc, submission_date=in_last_month, approval_date=in_this_month)
        Submission.objects.create(study_country=sc, submission_date=in_this_month, is_amendment=True)
        Submission.objects.create(study_country=sc, submission_date=too_old)                          # Out of range
        Submission.objects.create(study_country=sc, submission_date=in_this_month, not_applicable=True)  # Ignored

        months = self.get_dashboard()["submissionsByMonth"]

        self.assertEqual(len(months), SUBMISSIONS_MONTHS)
        self.assertEqual(months[-1], {"month": this_month.strftime("%Y-%m"), "submitted": 1, "approved": 1})
        self.assertEqual(months[-2], {"month": last_month.strftime("%Y-%m"), "submitted": 1, "approved": 0})
        self.assertEqual(sum(m["submitted"] for m in months), 2)

    def test_last_months_cross_year(self):
        months = DashboardView.get_last_months(13)
        self.assertEqual(len(months), 13)
        self.assertEqual(months[0].month, months[-1].month)   # Same month, one year apart
        self.assertEqual(months[0].year + 1, months[-1].year)

    # ---- Upcoming deadlines ----

    def test_upcoming_deadlines(self):
        ReportingPeriod.objects.create(project=self.project, stage=2, end=days_from_today(3))
        ReportingPeriod.objects.create(project=self.project, end=days_from_today(0))                     # Today
        ReportingPeriod.objects.create(project=self.project, end=days_from_today(-5))                    # Past
        ReportingPeriod.objects.create(project=self.project, end=days_from_today(DEADLINES_DAYS + 1))    # Too far
        ReportingPeriod.objects.create(end=days_from_today(DEADLINES_DAYS))                              # No project

        deadlines = self.get_dashboard()["upcomingDeadlines"]

        self.assertEqual(deadlines, [
            {"title": "Reporting period", "details": "Project A",
             "date": timezone.localdate().isoformat()},
            {"title": "Reporting period", "details": "Project A · Period 2",
             "date": (timezone.localdate() + timedelta(days=3)).isoformat()},
            {"title": "Reporting period", "details": "",
             "date": (timezone.localdate() + timedelta(days=DEADLINES_DAYS)).isoformat()},
        ])

    def test_upcoming_deadlines_ignore_visits(self):
        _, centre = self.create_centre()
        Visit.objects.create(centre=centre, visit_type=self.visit_type, visit_date=days_from_today(2))
        self.assertEqual(self.get_dashboard()["upcomingDeadlines"], [])

    def test_upcoming_deadlines_limit_and_order(self):
        for days in range(10, 0, -1):   # Created in reverse order
            ReportingPeriod.objects.create(project=self.project, end=days_from_today(days))

        deadlines = self.get_dashboard()["upcomingDeadlines"]

        self.assertEqual(len(deadlines), DEADLINES_LIMIT)
        dates = [deadline["date"] for deadline in deadlines]
        self.assertEqual(dates, sorted(dates))
        self.assertEqual(deadlines[0]["date"], (timezone.localdate() + timedelta(days=1)).isoformat())

    # ---- General ----

    def test_empty_database(self):
        data = self.get_dashboard()
        self.assertTrue(all(item["value"] == 0 for item in data["studiesByStatus"]))
        self.assertTrue(all(m["submitted"] == 0 and m["approved"] == 0 for m in data["submissionsByMonth"]))
        self.assertEqual(data["upcomingDeadlines"], [])

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.get(URL).status_code, (401, 403))

    def test_constant_number_of_queries(self):
        """Same number of SQL queries with 1 or 20 items of each kind"""
        def add_data(number):
            for i in range(number):
                sc, centre = self.create_centre(short_title=f"Study {i}")
                Study.objects.filter(pk=sc.study_id).update(status="Completed")
                Submission.objects.create(study_country=sc, submission_date=days_from_today(-1))
                Visit.objects.create(centre=centre, visit_type=self.visit_type, visit_date=days_from_today(i + 1))
                ReportingPeriod.objects.create(project=self.project, end=days_from_today(i + 1))

        add_data(1)
        with CaptureQueriesContext(connection) as small:
            self.get_dashboard()
        add_data(20)
        with CaptureQueriesContext(connection) as large:
            self.get_dashboard()

        self.assertEqual(len(small), len(large))
        self.assertLessEqual(len(large), 5)


class DashboardStudiesTests(APITestCase):
    """Studies of a status group, shown when clicking on the "Studies by status" chart"""

    URL = "/api/core/dashboard/studies"

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(short_name="Project A")
        cls.follow_up = Study.objects.create(short_title="B study", status="Running phase: Follow up", project=cls.project)
        cls.approvals = Study.objects.create(short_title="A study", status="Running phase: Regulatory & ethical approvals")
        cls.completed = Study.objects.create(short_title="C study", status="Completed", project=cls.project)
        cls.renamed = Study.objects.create(short_title="D study", status="Old renamed status")
        cls.empty = Study.objects.create(short_title="E study", status="  ")

    def setUp(self):
        self.client.force_authenticate(user=SimpleNamespace(is_authenticated=True))

    def get_studies(self, status_group):
        response = self.client.get(self.URL, {"status_group": status_group})
        self.assertEqual(response.status_code, 200)
        return response.json()["studies"]

    def test_studies_of_a_group_with_their_project(self):
        self.assertEqual(self.get_studies("Running"), [
            {"id": self.approvals.id, "shortTitle": "A study", "status": "Running phase: Regulatory & ethical approvals",
             "project": None},
            {"id": self.follow_up.id, "shortTitle": "B study", "status": "Running phase: Follow up",
             "project": {"id": self.project.id, "shortName": "Project A"}},
        ])

    def test_other_and_not_set_groups(self):
        self.assertEqual([s["id"] for s in self.get_studies("Other")], [self.renamed.id])
        self.assertEqual([s["id"] for s in self.get_studies("Not set")], [self.empty.id])

    def test_list_matches_chart_counts(self):
        """The list of each group has as many studies as the number shown on the chart"""
        counts = {item["name"]: item["value"] for item in self.client.get(URL).json()["studiesByStatus"]}
        for group, count in counts.items():
            self.assertEqual(len(self.get_studies(group)), count, group)

    def test_unknown_group(self):
        self.assertEqual(self.client.get(self.URL, {"status_group": "Unknown"}).status_code, 400)
        self.assertEqual(self.client.get(self.URL).status_code, 400)

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.get(self.URL, {"status_group": "Running"}).status_code, (401, 403))


class DashboardSubmissionsTests(APITestCase):
    """Submissions of a bar of the "Regulatory submissions" chart, shown when clicking on it"""

    URL = "/api/core/dashboard/submissions"

    @classmethod
    def setUpTestData(cls):
        cls.fr = Country.objects.create(iso2="FR", iso3="FRA", name="France")
        cls.ec = Authority.objects.create(code="EC", name="EC")
        cls.project = Project.objects.create(short_name="Project A")
        cls.study = Study.objects.create(short_title="Study A", project=cls.project)
        cls.sc = StudyCountry.objects.create(study=cls.study, country=cls.fr)

        last_month, this_month = DashboardView.get_last_months(2)
        cls.this_month, cls.last_month = this_month, last_month
        in_this_month = timezone.make_aware(datetime.combine(this_month, time(12)))
        in_last_month = timezone.make_aware(datetime.combine(last_month, time(12)))

        cls.initial = Submission.objects.create(study_country=cls.sc, authority=cls.ec,
                                                submission_date=in_last_month, approval_date=in_this_month)
        cls.amendment = Submission.objects.create(study_country=cls.sc, is_amendment=True, submission_date=in_this_month)
        Submission.objects.create(study_country=cls.sc, not_applicable=True, submission_date=in_this_month)  # Ignored

    def setUp(self):
        self.client.force_authenticate(user=SimpleNamespace(is_authenticated=True))

    def get_submissions(self, month, series):
        response = self.client.get(self.URL, {"month": month.strftime("%Y-%m"), "series": series})
        self.assertEqual(response.status_code, 200)
        return response.json()["submissions"]

    def test_submitted_of_a_month(self):
        self.assertEqual(self.get_submissions(self.last_month, "submitted"), [{
            "id": self.initial.id, "date": self.last_month.replace(day=1).isoformat(), "type": "Initial submission",
            "authority": "EC", "country": "France",
            "study": {"id": self.study.id, "shortTitle": "Study A"},
            "project": {"id": self.project.id, "shortName": "Project A"},
        }])
        self.assertEqual([s["id"] for s in self.get_submissions(self.this_month, "submitted")], [self.amendment.id])

    def test_approved_of_a_month(self):
        """A submission is listed in the month of its approval date, not of its submission date"""
        self.assertEqual([s["id"] for s in self.get_submissions(self.this_month, "approved")], [self.initial.id])
        self.assertEqual(self.get_submissions(self.last_month, "approved"), [])

    def test_lists_match_chart_bars(self):
        """Each bar has as many submissions in its list as its height"""
        months = DashboardView.get_last_months(SUBMISSIONS_MONTHS)
        bars = self.client.get(URL).json()["submissionsByMonth"]
        for month, bar in zip(months, bars):
            for series in ("submitted", "approved"):
                self.assertEqual(len(self.get_submissions(month, series)), bar[series], f"{bar['month']} {series}")

    def test_december_to_january(self):
        """The month after December is January of the next year"""
        december = date(2025, 12, 1)
        Submission.objects.create(study_country=self.sc, submission_date=timezone.make_aware(datetime(2025, 12, 31, 12)))
        Submission.objects.create(study_country=self.sc, submission_date=timezone.make_aware(datetime(2026, 1, 1, 12)))
        self.assertEqual(len(self.get_submissions(december, "submitted")), 1)

    def test_invalid_parameters(self):
        for params in ({"month": "2026-06", "series": "rejected"}, {"month": "June", "series": "submitted"},
                       {"series": "submitted"}, {}):
            self.assertEqual(self.client.get(self.URL, params).status_code, 400, params)

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.get(self.URL, {"month": "2026-06", "series": "submitted"}).status_code, (401, 403))
