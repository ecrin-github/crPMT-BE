import datetime

from django.db import models

from core.models.study import Study
from core.models.country import Country


class StudyCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_countries', default=None)
    country = models.CharField(max_length=255, blank=True, null=True)
    # TEMP
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL,
    #                                 db_column='country_id', blank=True, null=True,
    #                                 related_name='study_countries', default=None)
    lead_country = models.BooleanField(default=False, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'study_countries'
        ordering = ['id']
