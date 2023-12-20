from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from diophila import OpenAlex
# Create your models here.
from Essay.models import Author

gender_choices = [
    ('male','male'),
    ('female','female'),
]
class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10,choices=gender_choices,null=True,blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/',default='avatar/default.jpg', blank=True)
    avatar_url = models.CharField('用户头像路径', max_length=128, default='')
    register_date = models.DateTimeField(auto_now_add=True)

    is_professor = models.BooleanField(default=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author',null=True,blank=True) # 作者,开始可以为空
    work_count = models.IntegerField(default=0)
    is_administrators = models.BooleanField(default=False)
    
    unread_message_count = models.IntegerField(default=0)
