from django.db import models

from core.models.study import Study


class SatisfactionSurvey(models.Model):  # User satisfaction survey sent for a study (specs L2, issue #120)
    id = models.BigAutoField(primary_key=True)
    survey_type = models.CharField(max_length=255, blank=True, null=True)  # Initial / Follow-up / End of project
    number_of_recipients = models.PositiveIntegerField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        db_column="study_id",
        blank=True,
        null=True,
        related_name="satisfaction_surveys",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "satisfaction_surveys"
        ordering = ["order"]
