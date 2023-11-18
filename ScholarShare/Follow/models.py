from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# Create your models here.
from Essay.models import Author
from UserManage.models import User

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='followee')