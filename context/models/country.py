from django.db import models


class Country(models.Model):
    iso2 = models.CharField(max_length=2, primary_key=True)
    iso3 = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    continent = models.CharField(max_length=255, blank=True, null=True)
    is_in_eu = models.BooleanField(default=False)
    is_in_eea = models.BooleanField(default=False)

    class Meta:
        db_table = 'countries'
        ordering = ['iso2']
