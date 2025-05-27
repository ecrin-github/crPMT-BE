import datetime

from django.db import models

from context.models.ctu import CTU
from core.models.study import Study
from core.models.person import Person


class StudyCTU(models.Model):
    id = models.BigAutoField(primary_key=True)
    site_number = models.IntegerField(blank=True, null=True)
    patients_expected = models.IntegerField(blank=True, null=True)
    recruitment_greenlight = models.DateTimeField(default=False)
    mov_expected_number = models.IntegerField(blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_ctus', default=None)
    study_country = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_country_id', blank=True, null=True,
                                related_name='study_ctus', default=None)
    ctu = models.ForeignKey(CTU, on_delete=models.SET_NULL,
                                    db_column='ctu_id', blank=True, null=True,
                                    related_name='study_ctus', default=None)
    pi = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                    db_column='pi_id', blank=True, null=True,
                                    related_name='study_ctus', default=None)
    pi_national_coordinator = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'study_ctus'
        ordering = ['id']
