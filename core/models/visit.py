from django.db import models

from context.models.visit_type import VisitType
from core.models.centre import Centre


class Visit(models.Model):
    id = models.BigAutoField(primary_key=True)
    visit_type = models.ForeignKey(
        VisitType,
        on_delete=models.SET_NULL,
        db_column="visit_type",
        blank=True,
        null=True,
        related_name="visits",
        default=None,
    )
    visit_date = models.DateTimeField(blank=True, null=True)
    pharmacy = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    duration_unit = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    report_sent = models.BooleanField(default=False)
    report_sent_date = models.DateTimeField(blank=True, null=True)
    report_approved = models.BooleanField(default=False)
    report_approved_date = models.DateTimeField(blank=True, null=True)
    centre = models.ForeignKey(
        Centre,
        on_delete=models.CASCADE,
        db_column="centre_id",
        blank=True,
        null=True,
        related_name="visits",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "visits"
        # Note: multiple visits will have the same order (because) they are separated in the FE
        # but they will still be ordered correctly in the FE (because of this separation)
        ordering = ["order"]
