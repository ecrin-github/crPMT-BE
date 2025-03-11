import datetime

from django.db import models


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    ga_number = models.CharField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'projects'
        ordering = ['id']
