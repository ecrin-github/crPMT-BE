# Generated by Django 5.1.6 on 2025-03-06 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_end_project_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='GA_number',
            new_name='ga_number',
        ),
    ]
