# Generated by Django 5.2.3 on 2025-06-18 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("requests_app", "0002_request_notes_status_study_alter_request_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="status",
            name="study",
        ),
        migrations.AddField(
            model_name="study",
            name="status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="requests_app.status",
            ),
        ),
    ]
