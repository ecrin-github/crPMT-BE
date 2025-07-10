import datetime

from django.db import models

from context.models.country import Country
from core.models.study import Study


class StudyCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_countries', default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                    db_column='country_id', blank=True, null=True,
                                    related_name='study_countries', default=None)
    lead_country = models.BooleanField(default=False, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    class Meta:
        db_table = 'study_countries'
        ordering = ['order']
