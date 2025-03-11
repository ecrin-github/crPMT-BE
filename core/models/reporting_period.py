import datetime

from django.db import models

from core.models.project import Project


class ReportingPeriod(models.Model):
    id = models.BigAutoField(primary_key=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    stage = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                db_column='project_id', blank=True, null=True,
                                related_name='reporting_period_project_id', default=None)

    class Meta:
        db_table = 'reporting_periods'
        ordering = ['id']
