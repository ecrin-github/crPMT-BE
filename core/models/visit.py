import datetime

from django.db import models

from core.models.centre import Centre


class Visit(models.Model):
    id = models.BigAutoField(primary_key=True)
    visit_type = models.CharField(max_length=255,  db_column='type', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    greenlight = models.DateTimeField(blank=True, null=True)
    pharmacy = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    report_sent = models.DateTimeField(blank=True, null=True)
    report_approved = models.DateTimeField(blank=True, null=True)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE,
                                          db_column='centre_id', blank=True, null=True,
                                          related_name='visits', default=None)

    class Meta:
        db_table = 'visits'
        ordering = ['id']
