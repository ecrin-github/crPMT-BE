from django.db import models

from context.models.country import Country
from core.models.safety_notification import SafetyNotification
from core.models.study import Study


class StudyCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_countries', default=None)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, to_field="iso2",
                                    db_column='country_id', blank=True, null=True,
                                    related_name='study_countries', default=None)
    safety_notifications = models.ManyToManyField(SafetyNotification, related_name='study_countries', blank=True)
    sn_annual_ec_na = models.BooleanField(default=False)
    sn_annual_ca_na = models.BooleanField(default=False)
    sn_dsur_ec_na = models.BooleanField(default=False)
    sn_dsur_ca_na = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    class Meta:
        db_table = 'study_countries'
        ordering = ['order']