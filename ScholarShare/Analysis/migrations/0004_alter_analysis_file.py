# Generated by Django 4.2.4 on 2023-12-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Analysis", "0003_analysis_is_examined_analysis_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="analysis",
            name="file",
            field=models.FileField(
                default="", upload_to="data/analysis/", verbose_name="解析"
            ),
        ),
    ]
