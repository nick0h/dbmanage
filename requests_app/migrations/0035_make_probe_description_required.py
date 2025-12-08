# Generated manually

from django.db import migrations, models


def set_default_description(apps, schema_editor):
    """Set default description for any probes with NULL description"""
    Probe = apps.get_model('requests_app', 'Probe')
    Probe.objects.filter(description__isnull=True).update(description='')


class Migration(migrations.Migration):

    dependencies = [
        ("requests_app", "0034_make_antibody_fields_optional"),
    ]

    operations = [
        migrations.RunPython(set_default_description, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="probe",
            name="description",
            field=models.TextField(),
        ),
    ]



