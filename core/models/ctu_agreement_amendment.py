from django.db import models

from core.models.ctu_agreement import CTUAgreement


class CTUAgreementAmendment(models.Model):
    id = models.BigAutoField(primary_key=True)
    signed_date = models.DateTimeField(blank=True, null=True)
    ctu_agreement = models.ForeignKey(
        CTUAgreement,
        on_delete=models.CASCADE,
        db_column="ctu_agreement_id",
        blank=True,
        null=True,
        related_name="ctu_agreement_amendments",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "ctu_agremeent_amendments"
        ordering = ["order"]
