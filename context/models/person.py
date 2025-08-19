from django.db import models
from context.models.country import Country


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    is_euco = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                    db_column='country_id', blank=True, null=True,
                                    related_name='persons', default=None)

    class Meta:
        db_table = 'persons'
        ordering = ['id']