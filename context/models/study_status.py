from django.db import models


class StudyStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'study_statuses'
        ordering = ['id']
