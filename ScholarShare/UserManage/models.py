from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# Create your models here.

gender_choices = [
    ('male','male'),
    ('female','female'),
]
class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10,choices=gender_choices,null=True,blank=True)
    description = models.CharField(max_length=1000,null=True,blank=True)
    avatar = models.ImageField(upload_to='avatar/',default='avatar/default.jpg', blank=True)
    register_date = models.DateTimeField(auto_now_add=True)
