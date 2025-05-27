import datetime

from django.db import models

from context.models.country import Country
from core.models.study import Study


class Submission(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    approval = models.DateTimeField(blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)
    amendment = models.BooleanField(default=False)
    eotrial_notification = models.BooleanField(default=False)
    annual_progress_report = models.BooleanField(default=False)
    dsur = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                          db_column='country_id', blank=True, null=True,
                                          related_name='submission_country_id', default=None)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='submission_study_id', default=None)

    class Meta:
        db_table = 'submissions'
        ordering = ['id']
