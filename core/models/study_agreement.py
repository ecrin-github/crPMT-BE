from django.db import models

from core.models.study import Study


class StudyAgreement(models.Model):
    id = models.BigAutoField(primary_key=True)
    draft_sent_date = models.DateTimeField(blank=True, null=True)
    signed_by_sponsor_date = models.DateTimeField(blank=True, null=True)
    signed_by_ecrin_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        db_column="study_id",
        blank=True,
        null=True,
        related_name="study_agreements",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    @property
    def fully_executed(self):
        # Automatically true once both Sponsor and ECRIN signature dates are entered
        return bool(self.signed_by_sponsor_date and self.signed_by_ecrin_date)

    class Meta:
        db_table = "study_agreements"
        ordering = ["order"]
