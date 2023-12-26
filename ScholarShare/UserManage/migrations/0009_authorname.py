# Generated by Django 4.2.4 on 2023-12-25 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("UserManage", "0008_rename_search_history_language_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthorName",
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
                ("name", models.CharField(default="", max_length=255)),
                (
                    "history",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UserManage.history",
                    ),
                ),
            ],
        ),
    ]