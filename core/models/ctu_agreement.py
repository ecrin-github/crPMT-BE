from django.db import models

from context.models.ctu_status import CTUStatus
from core.models.study_ctu import StudyCTU


class CTUAgreement(models.Model):
    id = models.BigAutoField(primary_key=True)
    signed = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    ctu_status = models.ForeignKey(
        CTUStatus,
        on_delete=models.SET_NULL,
        db_column="ctu_status_id",
        blank=True,
        null=True,
        related_name="ctu_agreements",
        default=None,
    )
    study_ctu = models.ForeignKey(
        StudyCTU,
        on_delete=models.CASCADE,
        db_column="study_ctu_id",
        blank=True,
        null=True,
        related_name="ctu_agreements",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "ctu_agreements"
        ordering = ["order"]
