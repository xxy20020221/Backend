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
    ('male', 'male'),
    ('female', 'female'),
]


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg', blank=True)
    avatar_url = models.CharField('用户头像路径', max_length=128, default='')
    register_date = models.DateTimeField(auto_now_add=True)

    is_professional = models.IntegerField('是否认证', default=-1)  # -1未认证，0正在申请，1已认证
    is_professor = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author', null=True,
                               blank=True)  # 作者,开始可以为空
    work_count = models.IntegerField(default=0)
    is_administrators = models.BooleanField(default=False)

    unread_message_count = models.IntegerField(default=0)


class History(models.Model):
    #
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    title = models.CharField(default='', max_length=255)
    publication_date = models.CharField(default='', max_length=255)
    language = models.CharField(default='', max_length=255)
    open_alex_id = models.CharField(default='', max_length=255)
    author_name = models.TextField(default='', max_length=255)
    cited_by_count = models.IntegerField(default=0)

class AuthorName(models.Model):
    history = models.ForeignKey("History", on_delete=models.CASCADE, null=True)
    name = models.CharField(default='', max_length=255)