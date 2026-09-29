from django.db import migrations

# Initial fixed set of values for the "ECRIN contracting entity" dropdown (#92, spec L2-2.1).
# TODO: this list is provisional and should be reviewed/completed later - the "Add" option
# has been removed from the UI on purpose so it can only be extended here or via the admin.
VALUES = [
    "Beneficiary",
    "Subcontractor",
    "Other",
]


def seed_values(apps, schema_editor):
    EcrinContractingEntity = apps.get_model('context', 'EcrinContractingEntity')
    for value in VALUES:
        EcrinContractingEntity.objects.get_or_create(value=value)


def remove_values(apps, schema_editor):
    EcrinContractingEntity = apps.get_model('context', 'EcrinContractingEntity')
    EcrinContractingEntity.objects.filter(value__in=VALUES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0028_merge_20260918_1233'),
    ]

    operations = [
        migrations.RunPython(seed_values, remove_values),
    ]
