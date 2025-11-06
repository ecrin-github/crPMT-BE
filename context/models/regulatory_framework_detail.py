from django.db import models


class RegulatoryFrameworkDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'regulatory_framework_details'
        ordering = ['id']
