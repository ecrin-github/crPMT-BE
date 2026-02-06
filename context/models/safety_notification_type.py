from django.db import models


class SafetyNotificationType(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'safety_notification_types'
        ordering = ['code']
