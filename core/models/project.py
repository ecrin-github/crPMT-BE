import datetime

from django.db import models

from context.models.funding_source import FundingSource
from context.models.organisation import Organisation
from context.models.person import Person
from context.models.service import Service


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    # General information
    short_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    coordinating_institution = models.ForeignKey(Organisation, on_delete=models.SET_NULL,
                                    db_column='coordinating_institution_id', blank=True, null=True,
                                    related_name='projects', default=None)
    coordinator = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                    db_column='coordinator_id', blank=True, null=True,
                                    related_name='projects', default=None)

    # Project funding
    funding_sources = models.ManyToManyField(FundingSource, blank=True)
    ga_number = models.CharField(blank=True, null=True)

    # Publication information
    public_summary = models.CharField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'projects'
        ordering = ['id']
