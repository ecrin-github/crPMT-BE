from django.db import models


class Authority(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'authorities'
        ordering = ['code']
