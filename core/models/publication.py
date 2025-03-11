from django.db import models

from core.models.study import Study
from core.models.project import Project


class Publication(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    pubmed = models.CharField(max_length=255, blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='publication_study_id', default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                db_column='project_id', blank=True, null=True,
                                related_name='publication_project_id', default=None)

    class Meta:
        db_table = 'publications'
        ordering = ['id']
