from django.db import models

from context.models.ctu_status import CTUStatus
from core.models.study_ctu import StudyCTU


class CTUAgreement(models.Model):
    id = models.BigAutoField(primary_key=True)
    signed = models.BooleanField(default=False)  # Deprecated, superseded by fully_executed (see #96)
    draft_sent_date = models.DateTimeField(blank=True, null=True)
    signed_by_ctu_date = models.DateTimeField(blank=True, null=True)
    signed_by_ecrin_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    ctu_status = models.ForeignKey(  # Deprecated, unrelated to the spec's "contract status" (see #96)
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

    @property
    def fully_executed(self):
        # Automatically true once both CTU and ECRIN signature dates are entered
        return bool(self.signed_by_ctu_date and self.signed_by_ecrin_date)

    class Meta:
        db_table = "ctu_agreements"
        ordering = ["order"]
