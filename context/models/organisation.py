from django.db import models

from context.models.country import Country


class Organisation(models.Model):
    id = models.BigAutoField(primary_key=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                    db_column='country_id', blank=True, null=True,
                                    related_name='organisations', default=None)

    class Meta:
        db_table = 'organisations'
        ordering = ['id']
