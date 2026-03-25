from django.db import models

from core.models.study import Study
from core.models.project import Project


class Publication(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    pubmed_url = models.CharField(max_length=500, blank=True, null=True)

    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        db_column='study_id',
        blank=True,
        null=True,
        related_name='publications',
        default=None
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        db_column='project_id',
        blank=True,
        null=True,
        related_name='publications',
        default=None
    )

    class Meta:
        db_table = 'publications'
        ordering = ['id']

    def __str__(self):
        return self.title or f'Publication {self.id}'