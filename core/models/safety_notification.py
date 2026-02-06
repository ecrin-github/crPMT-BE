import datetime

from django.db import models

from context.models.authority import Authority
from context.models.safety_notification_type import SafetyNotificationType

class SafetyNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL,
                                db_column='authority_id', blank=True, null=True,
                                related_name='safety_notifications', default=None)
    year = models.CharField(max_length=100, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    not_applicable = models.BooleanField(default=False)
    notification_type = models.ForeignKey(SafetyNotificationType, on_delete=models.SET_NULL,
                                db_column='safety_notification_type_id', blank=True, null=True,
                                related_name='safety_notifications', default=None)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    class Meta:
        db_table = 'safety_notifications'
        ordering = ['order']
