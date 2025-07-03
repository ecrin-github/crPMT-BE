import datetime

from django.db import models

from context.models.funding_source import FundingSource
from context.models.service import Service
from core.models.person import Person


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    ga_number = models.CharField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    total_patients_expected = models.CharField(max_length=255, blank=True, null=True)
    funding_sources = models.ManyToManyField(FundingSource, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    c_euco = models.ForeignKey(Person, on_delete=models.SET_NULL, unique=False, editable=True,
                                    blank=True, null=True, db_index=True,
                                    db_column='c_euco_id', related_name='projects', default=None)
    
    class Meta:
        db_table = 'projects'
        ordering = ['id']
