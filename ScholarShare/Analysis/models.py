from django.db import models

from ScholarShare.Essay.models import Work
from ScholarShare.UserManage.models import User


# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis')
    works = models.ManyToManyField(Work, related_name='works', through='Collection', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    file_url = models.CharField(default='', max_length=128, verbose_name='路径')
    file = models.FileField(default='', upload_to='analysis/', verbose_name='解析')

    class Meta:
        db_table = 'Analysis'