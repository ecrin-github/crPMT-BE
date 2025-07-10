import datetime

from django.db import models

from context.models.person import Person
from core.models.study_ctu import StudyCTU


class Centre(models.Model):
    id = models.BigAutoField(primary_key=True)
    site_number = models.CharField(max_length=255, blank=True, null=True)
    patients_expected = models.CharField(max_length=255, blank=True, null=True)
    recruitment_greenlight = models.DateTimeField(blank=True, null=True)
    mov_expected_number = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(blank=True, null=True)
    hospital = models.CharField(blank=True, null=True)
    first_patient_visit = models.DateTimeField(blank=True, null=True)
    study_ctu = models.ForeignKey(StudyCTU, on_delete=models.SET_NULL,
                                    db_column='study_ctu_id', blank=True, null=True,
                                    related_name='centres', default=None)
    pi = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                    db_column='pi_id', blank=True, null=True,
                                    related_name='centres', default=None)
    pi_national_coordinator = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True, db_column='order')
    
    class Meta:
        db_table = 'centres'
        ordering = ['order']
