from django.db import models

from core.models.project import Project


class Publication(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    pubmed_url = models.CharField(max_length=500, blank=True, null=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        db_column='project_id',
        blank=True,
        null=True,
        related_name='publications',
        default=None
    )

    order = models.IntegerField(blank=True, null=True)

    publication_acknowledging_ecrin = models.BooleanField(default=False)
    ecrin_employee_in_authors = models.BooleanField(default=False)

    class Meta:
        db_table = 'publications'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f'Publication {self.id}'