from rest_framework import serializers
from .models import Message
from UserManage.serializers import ShortUserSerializer
from datetime import datetime
import string
import os 

class MessageSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    sender = ShortUserSerializer()
    receiver = ShortUserSerializer()
    class Meta:
        model = Message
        fields = ['id','sender','receiver','content','reply','created_time','is_read']

    