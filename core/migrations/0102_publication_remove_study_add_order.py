from django.db import migrations, models


def migrate_publication_project(apps, schema_editor):
    Publication = apps.get_model('core', 'Publication')
    Study = apps.get_model('core', 'Study')

    for publication in Publication.objects.filter(project__isnull=True).exclude(study__isnull=True):
        study = Study.objects.filter(pk=publication.study_id).first()
        if study and study.project_id is not None:
            publication.project_id = study.project_id
            publication.save(update_fields=['project_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0101_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(migrate_publication_project, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='publication',
            name='study',
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'db_table': 'publications', 'ordering': ['order', 'id']},
        ),
    ]
