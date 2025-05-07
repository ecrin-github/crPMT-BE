from django.db import models

from core.models.country import Country
from core.models.person import Person


class CTU(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    address_info = models.TextField(blank=True, null=True)
    sas_verification = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                    db_column='country_id', blank=True, null=True,
                                    related_name='ctu_country_id', default=None)
    contact = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                    db_column='contact_id', blank=True, null=True,
                                    related_name='ctu_study_id', default=None)

    class Meta:
        db_table = 'ctus'
        ordering = ['id']
