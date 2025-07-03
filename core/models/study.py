from django.db import models

from core.models.person import Person
from core.models.project import Project


class Study(models.Model):
    id = models.BigAutoField(primary_key=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    
    sponsor = models.CharField(max_length=255, blank=True, null=True)
    regulatory_framework = models.CharField(max_length=255, blank=True, null=True)
    trial_id = models.CharField(max_length=255, blank=True, null=True)  # Missing from the model?
    summary = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    population = models.CharField(max_length=255, blank=True, null=True)
    recruitment_start = models.DateTimeField(blank=True, null=True)
    recruitment_end = models.DateTimeField(blank=True, null=True)
    first_patient_in = models.DateTimeField(blank=True, null=True)
    first_patient_out = models.DateTimeField(blank=True, null=True)
    # Trial registration?
    project = models.ForeignKey(Project, on_delete=models.CASCADE, unique=False, editable=True,
                                    blank=True, null=True, db_index=True,
                                    db_column='project_id', related_name='studies', default=None)
    pi = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                db_column='pi_id', blank=True, null=True,
                                related_name='study_pi_id', default=None)
    order = models.IntegerField(blank=True, null=True, db_column='s_order')

    class Meta:
        db_table = 'studies'
        ordering = ['id', 'order']
