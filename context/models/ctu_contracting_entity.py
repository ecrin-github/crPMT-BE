from django.db import models


class CtuContractingEntity(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'ctu_contracting_entities'
        ordering = ['id']
