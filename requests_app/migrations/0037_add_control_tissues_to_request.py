from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requests_app', '0036_add_data_field_to_embedding_sectioning'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='positive_control_tissue',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='positive_control_requests',
                to='requests_app.tissue',
                verbose_name='Positive Control Tissue',
            ),
        ),
        migrations.AddField(
            model_name='request',
            name='negative_control_tissue',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='negative_control_requests',
                to='requests_app.tissue',
                verbose_name='Negative Control Tissue',
            ),
        ),
    ]
