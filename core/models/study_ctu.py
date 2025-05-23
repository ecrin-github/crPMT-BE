import datetime

from django.db import models

from context.models.ctu import CTU
from core.models.study import Study


class StudyCTU(models.Model):
    id = models.BigAutoField(primary_key=True)
    patient_expected = models.IntegerField(blank=True, null=True)
    mov_greenlight = models.DateTimeField(blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_ctu_study_id', default=None)
    ctu = models.ForeignKey(CTU, on_delete=models.SET_NULL,
                                    db_column='ctu_id', blank=True, null=True,
                                    related_name='study_ctu_ctu_id', default=None)
    
    class Meta:
        db_table = 'study_ctus'
        ordering = ['id']
