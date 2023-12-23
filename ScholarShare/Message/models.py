from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# Create your models here.
from Analysis.models import Analysis
from UserManage.models import User
from Essay.models import Work,Author,Institution
class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender',null=True) # 自己的id
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver',null=True) # 回复的用户id
    send_time = models.DateTimeField(auto_now_add=True) # 评论时间
    type = models.IntegerField(default=0)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='analysis',null=True) #解析id
    # 消息类型： 0表示申请通过，1表示申请拒绝，2表示有消息被回复，3表示有解析被上传，4表示有文章被回复，5表示有有用户关注了你, 6表示有解析需要被审核,7表示解析审核失败,8表示解析审核成功, 9表示有解析被回复,10表示有认证需要被审核

    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='message_author',null=True) # 作者id
    open_alex_id = models.CharField('对应作者的open_alex_id', max_length=200, db_index=True,
                                    default='')
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name='message_institution',null=True) # 机构id
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='message_work',null=True) # 文章id

    content = models.TextField(max_length=1024,default="")  #消息内容
    reply = models.TextField(max_length=1024,default="")  #回复内容(如果是回复消息的话)
    
    pdf = models.FileField(max_length=100,upload_to='confirm/',default="")  #pdf
    url = models.CharField(max_length=100,default="")  #访问路由
    is_read = models.BooleanField(default=False)


