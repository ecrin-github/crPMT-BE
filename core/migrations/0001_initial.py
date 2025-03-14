# Generated by Django 5.1.6 on 2025-03-04 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('GA_number', models.IntegerField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'projects',
                'ordering': ['id'],
            },
        ),
    ]
