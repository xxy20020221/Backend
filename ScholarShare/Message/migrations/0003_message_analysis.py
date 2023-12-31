# Generated by Django 4.1 on 2023-12-19 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Analysis", "0003_analysis_is_examined_analysis_title"),
        ("Message", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="analysis",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis",
                to="Analysis.analysis",
            ),
        ),
    ]
