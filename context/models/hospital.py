from django.db import models
from context.models.country import Country


class Hospital(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                    db_column='country_id', blank=True, null=True,
                                    related_name='hospitals', default=None)

    class Meta:
        db_table = 'hospitals'
        ordering = ['id']