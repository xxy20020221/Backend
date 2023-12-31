# Generated by Django 4.2.4 on 2023-12-21 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Comment", "0003_commenttocomment_analysis_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="commenttocomment", name="comment",),
        migrations.RemoveField(model_name="commenttowork", name="work",),
        migrations.AddField(
            model_name="commenttocomment",
            name="work_openalex_id",
            field=models.CharField(default="", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="commenttowork",
            name="work_openalex_id",
            field=models.CharField(default="", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="commenttocomment",
            name="father",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_to_comment",
                to="Comment.comment",
            ),
        ),
    ]
