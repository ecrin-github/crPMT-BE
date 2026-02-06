from django.db import models


class CTUStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'ctu_statuses'
        ordering = ['id']
