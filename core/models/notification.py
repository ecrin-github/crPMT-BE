from django.db import models

from context.models.authority import Authority
from core.models.study_country import StudyCountry


class Notification(models.Model):  # End of trial notification
    id = models.BigAutoField(primary_key=True)
    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL,
                                db_column='authority_id', blank=True, null=True,
                                related_name='notifications', default=None)
    notification_date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    study_country = models.ForeignKey(
        StudyCountry,
        on_delete=models.CASCADE,
        db_column="study_country_id",
        blank=True,
        null=True,
        related_name="notifications",
        default=None,
    )
    order = models.IntegerField(blank=True, null=True, db_column="order")

    class Meta:
        db_table = "notifications"
        ordering = ["order"]
