from types import SimpleNamespace

from rest_framework.test import APITestCase

from core.models.ctu_agreement_amendment import CTUAgreementAmendment
from core.models.notification import Notification
from core.models.publication import Publication
from core.models.reporting_period import ReportingPeriod
from core.models.safety_notification import SafetyNotification
from core.models.study_agreement_amendment import StudyAgreementAmendment
from core.models.submission import Submission
from core.models.visit import Visit


class BulkDeleteTestMixin:
    model = None
    url = None

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=SimpleNamespace(is_authenticated=True))

    def create_objects(self):
        return [self.model.objects.create() for _ in range(2)]

    def test_bulk_delete_two_ids(self):
        objects = self.create_objects()

        response = self.client.post(
            f"{self.url}/bulk_delete",
            {"ids": [obj.pk for obj in objects]},
            format="json",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.model.objects.count(), 0)

    def test_bulk_delete_unknown_id_deletes_nothing(self):
        objects = self.create_objects()

        response = self.client.post(
            f"{self.url}/bulk_delete",
            {"ids": [objects[0].pk, max(obj.pk for obj in objects) + 1000]},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.model.objects.count(), 2)

    def test_bulk_delete_invalid_payloads(self):
        objects = self.create_objects()
        invalid_payloads = ({"ids": "x"}, [], {})

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    f"{self.url}/bulk_delete", payload, format="json"
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.model.objects.count(), 2)


class BulkEndpointTestMixin(BulkDeleteTestMixin):
    value_field = "order"
    invalid_field = "order"

    def payload(self, value):
        return {self.value_field: value}

    def test_bulk_create_two_objects(self):
        response = self.client.post(
            f"{self.url}/bulk_create",
            [self.payload(101), self.payload(102)],
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.model.objects.count(), 2)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all("id" in item for item in response.data))

    def test_bulk_create_rejects_non_list_body(self):
        response = self.client.post(
            f"{self.url}/bulk_create", {self.value_field: 101}, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.model.objects.count(), 0)

    def test_bulk_create_invalid_item_creates_nothing(self):
        invalid = {self.invalid_field: "not-an-integer"}

        response = self.client.post(
            f"{self.url}/bulk_create",
            [self.payload(101), invalid],
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.model.objects.count(), 0)

    def test_bulk_update_two_objects(self):
        objects = [
            self.model.objects.create(**self.payload(1)),
            self.model.objects.create(**self.payload(2)),
        ]

        response = self.client.put(
            f"{self.url}/bulk_update",
            [
                {"id": objects[0].pk, **self.payload(11)},
                {"id": objects[1].pk, **self.payload(12)},
            ],
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(
                self.model.objects.order_by("pk").values_list(
                    self.value_field, flat=True
                )
            ),
            [11, 12],
        )

    def test_bulk_update_unknown_id_does_not_update_valid_item(self):
        obj = self.model.objects.create(**self.payload(1))
        unknown_id = obj.pk + 1000

        response = self.client.put(
            f"{self.url}/bulk_update",
            [
                {"id": obj.pk, **self.payload(11)},
                {"id": unknown_id, **self.payload(12)},
            ],
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        obj.refresh_from_db()
        self.assertEqual(getattr(obj, self.value_field), 1)

    def test_bulk_update_requires_id(self):
        obj = self.model.objects.create(**self.payload(1))

        response = self.client.put(
            f"{self.url}/bulk_update", [self.payload(11)], format="json"
        )

        self.assertEqual(response.status_code, 400)
        obj.refresh_from_db()
        self.assertEqual(getattr(obj, self.value_field), 1)


class CTUAgreementAmendmentBulkTests(BulkEndpointTestMixin, APITestCase):
    model = CTUAgreementAmendment
    url = "/api/core/ctu-agreement-amendments"


class StudyAgreementAmendmentBulkTests(BulkEndpointTestMixin, APITestCase):
    model = StudyAgreementAmendment
    url = "/api/core/study-agreement-amendments"


class ReportingPeriodBulkTests(BulkEndpointTestMixin, APITestCase):
    model = ReportingPeriod
    url = "/api/core/reporting-periods"
    value_field = "stage"
    invalid_field = "stage"


class PublicationBulkTests(BulkEndpointTestMixin, APITestCase):
    model = Publication
    url = "/api/core/publications"


class NotificationBulkTests(BulkEndpointTestMixin, APITestCase):
    model = Notification
    url = "/api/core/notifications"


class SafetyNotificationBulkTests(BulkEndpointTestMixin, APITestCase):
    model = SafetyNotification
    url = "/api/core/safety-notifications"


class SubmissionBulkTests(BulkEndpointTestMixin, APITestCase):
    model = Submission
    url = "/api/core/submissions"


class VisitBulkDeleteTests(BulkDeleteTestMixin, APITestCase):
    model = Visit
    url = "/api/core/visits"