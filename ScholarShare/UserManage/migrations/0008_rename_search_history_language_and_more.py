# Generated by Django 4.2.4 on 2023-12-25 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UserManage", "0007_alter_user_avatar_history"),
    ]

    operations = [
        migrations.RenameField(
            model_name="history",
            old_name="search",
            new_name="language",
        ),
        migrations.RemoveField(
            model_name="history",
            name="is_advanced",
        ),
        migrations.RemoveField(
            model_name="history",
            name="type",
        ),
        migrations.AddField(
            model_name="history",
            name="author_name",
            field=models.TextField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="history",
            name="cited_by_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="history",
            name="open_alex_id",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="history",
            name="publication_date",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="history",
            name="title",
            field=models.CharField(default="", max_length=255),
        ),
    ]