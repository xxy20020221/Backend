from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# Create your models here.
from UserManage.models import User
from Essay.models import Work,Author,Institution
class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender',null=True) # 自己的id
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver',null=True) # 回复的用户id
    send_time = models.DateTimeField(auto_now_add=True) # 评论时间
    type = models.IntegerField(default=0) 
    # 消息类型： 0表示申请通过，1表示申请拒绝，2表示有消息被回复，3表示有解析被上传，4表示有文章被回复，5表示有有用户关注了你

    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='message_author',null=True) # 作者id
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name='message_institution',null=True) # 机构id
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='message_work',null=True) # 文章id

    content = models.TextField(max_length=1024,default="")  #消息内容
    reply = models.TextField(max_length=1024,default="")  #回复内容(如果是回复消息的话)
    
    pdf = models.CharField(max_length=100,default="")  #pdf
    url = models.CharField(max_length=100,default="")  #访问路由


