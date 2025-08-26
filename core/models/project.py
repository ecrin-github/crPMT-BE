import datetime

from django.db import models

from context.models.funding_source import FundingSource
from context.models.organisation import Organisation
from context.models.person import Person
from context.models.service import Service


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    # General information
    name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    coordinator = models.ForeignKey(Organisation, on_delete=models.SET_NULL,
                                    db_column='organisation_id', blank=True, null=True,
                                    related_name='projects', default=None)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # Project funding
    funding_sources = models.ManyToManyField(FundingSource, blank=True)
    ga_number = models.CharField(blank=True, null=True)

    # Publication information
    public_summary = models.CharField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    total_patients_expected = models.CharField(max_length=255, blank=True, null=True)   # TODO: remove?
    
    class Meta:
        db_table = 'projects'
        ordering = ['id']
