from django.db import models


class VisitType(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'visit_types'
        ordering = ['code']
