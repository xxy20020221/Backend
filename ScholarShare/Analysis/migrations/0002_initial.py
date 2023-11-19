# Generated by Django 4.1 on 2023-11-19 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Analysis", "0001_initial"),
        ("Essay", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="analysis",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="analysis",
            name="works",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="works",
                to="Essay.work",
            ),
        ),
    ]
