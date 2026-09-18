from django.db import migrations

# Initial fixed set of values for the "CTU contracting entity" dropdown (#95, spec L4a-3.1).
# TODO: this list is provisional and should be reviewed/completed later - the "Add" option
# has been removed from the UI on purpose so it can only be extended here or via the admin.
VALUES = [
    "Beneficiary",
    "Subcontractor",
    "Affiliate entity",
    "In kind contribution",
    "Other",
]


def seed_values(apps, schema_editor):
    CtuContractingEntity = apps.get_model('context', 'CtuContractingEntity')
    for value in VALUES:
        CtuContractingEntity.objects.get_or_create(value=value)


def remove_values(apps, schema_editor):
    CtuContractingEntity = apps.get_model('context', 'CtuContractingEntity')
    CtuContractingEntity.objects.filter(value__in=VALUES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0025_ctucontractingentity'),
    ]

    operations = [
        migrations.RunPython(seed_values, remove_values),
    ]
