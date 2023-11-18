from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from diophila import OpenAlex
# Create your models here.
from UserManage.models import User
from Essay.models import Work
from Analysis.models import Analysis

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment') # 自己的id
    replied_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='replied_user',null=True,blank=True) # 回复的用户id
    type = models.IntegerField(default=0) # 评论类型 0：文章 1：解析 2:回复
    level = models.IntegerField(default=0)  # 评论等级
    created_time = models.DateTimeField(auto_now_add=True) # 评论时间
    content = models.TextField(max_length=1024,default="")  #评论内容


class CommentToWork(Comment):
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='comment_to_work',null=True,blank=True) # 文章id

class CommentToAnalysis(Comment):
    analysis = models.ForeignKey(Analysis,on_delete=models.CASCADE,related_name='comment_to_analysis',null=True,blank=True) # 解析id

class CommentToComment(Comment):
    father = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='children',null=True,blank=True) # 上级work或analysis的id
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment_to_comment',null=True,blank=True) # 父评论id

    
