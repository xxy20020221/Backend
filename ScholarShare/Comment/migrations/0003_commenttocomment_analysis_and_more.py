# Generated by Django 4.2.4 on 2023-12-19 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Essay', '0001_initial'),
        ('Analysis', '0003_analysis_is_examined_analysis_title'),
        ('Comment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commenttocomment',
            name='analysis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='anaylysis_comment_father', to='Analysis.analysis'),
        ),
        migrations.AlterField(
            model_name='commenttocomment',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_comment_father', to='Essay.work'),
        ),
    ]