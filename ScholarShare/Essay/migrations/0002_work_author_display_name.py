# Generated by Django 4.2.4 on 2023-12-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Essay", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="author_display_name",
            field=models.CharField(default="", max_length=200),
        ),
    ]