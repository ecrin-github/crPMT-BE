from django.db import models

from core.models.study_agreement import StudyAgreement


class StudyAgreementAmendment(models.Model):
    id = models.BigAutoField(primary_key=True)
    signed_by_sponsor_date = models.DateTimeField(blank=True, null=True)
    signed_by_ecrin_date = models.DateTimeField(blank=True, null=True)
    new_end_date = models.DateTimeField(blank=True, null=True)
    study_agreement = models.ForeignKey(
        StudyAgreement,
        on_delete=models.CASCADE,
        db_column="study_agreement_id",
        blank=True,
        null=True,
        related_name="study_agreement_amendments",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "study_agreement_amendments"
        ordering = ["order"]
