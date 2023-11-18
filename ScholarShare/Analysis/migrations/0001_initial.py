# Generated by Django 4.2.4 on 2023-11-18 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Essay", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "file_url",
                    models.CharField(default="", max_length=128, verbose_name="路径"),
                ),
                (
                    "file",
                    models.FileField(
                        default="", upload_to="analysis/", verbose_name="解析"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analysis",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "works",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="works",
                        to="Essay.work",
                    ),
                ),
            ],
            options={"db_table": "Analysis",},
        ),
    ]
