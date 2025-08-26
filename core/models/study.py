from django.db import models

from context.models.complex_trial_type import ComplexTrialType
from context.models.country import Country
from context.models.medical_field import MedicalField
from context.models.organisation import Organisation
from context.models.person import Person
from context.models.population import Population
from context.models.service import Service
from core.models.project import Project


class Study(models.Model):
    id = models.BigAutoField(primary_key=True)
    # General study information
    title = models.TextField(blank=True, null=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    sponsor_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE,
                                    db_column='organisation_id', blank=True, null=True,
                                    related_name='studies', default=None)
    pi = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                db_column='pi_id', blank=True, null=True,
                                related_name='studies', default=None)
    sponsor_country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                    db_column='sponsor_country_id', blank=True, null=True,
                                    related_name='persons', default=None)
    medical_fields = models.ManyToManyField(MedicalField, blank=True)
    populations = models.ManyToManyField(Population, blank=True)
    rare_diseases = models.BooleanField(default=False)
    regulatory_framework = models.CharField(max_length=255, blank=True, null=True)
    complex_trial_design = models.BooleanField(default=False)
    complex_trial_type = models.ForeignKey(ComplexTrialType, on_delete=models.CASCADE,
                                    db_column='complex_trial_type_id', blank=True, null=True,
                                    related_name='studies', default=None)
    trial_registration_number = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)   # Note: missing from specs

    # Country, site information
    c_euco = models.ForeignKey(Person, on_delete=models.SET_NULL, unique=False, editable=True,
                                blank=True, null=True, db_index=True,
                                db_column='c_euco_id', related_name='studies', default=None)
    coordinating_country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                    db_column='coordinating_country_id', blank=True, null=True,
                                    related_name='studies', default=None)
    services = models.ManyToManyField(Service, blank=True)

    # Clinical study timelines
    # TODO: check specs for recruitment period
    recruitment_start = models.DateTimeField(blank=True, null=True)
    recruitment_end = models.DateTimeField(blank=True, null=True)
    treatment_duration_per_patient = models.CharField(blank=True, null=True)
    treatment_duration_per_patient_unit = models.CharField(blank=True, null=True)
    treatment_and_follow_up_duration_per_patient = models.CharField(blank=True, null=True)
    treatment_and_follow_up_duration_per_patient_unit = models.CharField(blank=True, null=True)
    first_patient_in = models.DateTimeField(blank=True, null=True)
    last_patient_out = models.DateTimeField(blank=True, null=True)

    # Overall status
    status = models.CharField(max_length=255, blank=True, null=True)

    # Internal
    project = models.ForeignKey(Project, on_delete=models.CASCADE, unique=False, editable=True,
                                    blank=True, null=True, db_index=True,
                                    db_column='project_id', related_name='studies', default=None)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    class Meta:
        db_table = 'studies'
        ordering = ['order']
