import datetime

from django.db import models
from context.models.ctu import CTU
from core.models.study_country import StudyCountry
from core.models.study import Study


class StudyCTU(models.Model):
    id = models.BigAutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_ctus', default=None)
    study_country = models.ForeignKey(StudyCountry, on_delete=models.CASCADE,
                                    db_column='study_country_id', blank=True, null=True,
                                    related_name='study_ctus', default=None)
    ctu = models.ForeignKey(CTU, on_delete=models.CASCADE,
                                    db_column='ctu_id', blank=True, null=True,
                                    related_name='study_ctus', default=None)
    order = models.IntegerField(blank=True, null=True, db_column='order')
    # Many-to-one with Centre, FK in Centre
    
    class Meta:
        db_table = 'study_ctus'
        ordering = ['order']
