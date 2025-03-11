from django.db import models


class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'countries'
        ordering = ['id']
