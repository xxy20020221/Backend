from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# Create your models here.
from Essay.models import Work
from UserManage.models import User
from Analysis.models import Analysis

class ColletionPackage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user') # 自己的id
    works = models.ManyToManyField(Work,through='CollectionWork',related_name="collection_package_work",blank=True)
    anaylsis = models.ManyToManyField(Analysis,through='CollectionAnalysis',related_name="collection_package_analysis",blank=True)
    created_time = models.DateTimeField(auto_now_add=True) # 评论时间
    name = models.CharField(max_length=100,default="")  #评论内容
    sum = models.IntegerField(default=0)  #评论数量


class CollectionWork(models.Model):
    
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='collection_work') # 文章id
    collection_package = models.ForeignKey(ColletionPackage,on_delete=models.CASCADE,related_name='collectionpackage_work') # 文章id
    created_time = models.DateTimeField(auto_now_add=True) # 评论时间
    class Meta:
        unique_together = ('work','collection_package')

class CollectionAnalysis(models.Model):
    
    analysis = models.ForeignKey(Analysis,on_delete=models.CASCADE,related_name='collection_analysis') # 文章id
    collection_package = models.ForeignKey(ColletionPackage,on_delete=models.CASCADE,related_name='collectionpackage_analysis') # 文章id
    created_time = models.DateTimeField(auto_now_add=True) # 评论时间
    class Meta:
        unique_together = ('analysis','collection_package')
