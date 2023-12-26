# Generated by Django 4.2.4 on 2023-12-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UserManage", "0009_authorname"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="true_man",
            field=models.ImageField(
                blank=True, default="true/default.jpg", upload_to="true/"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="true_man_url",
            field=models.CharField(default="", max_length=128, verbose_name="用户真人头像路径"),
        ),
    ]