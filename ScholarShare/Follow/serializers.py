from rest_framework import serializers
from .models import CollectionAnalysis,CollectionWork,ColletionPackage
from Essay.models import Work
from datetime import datetime
import string
import os 
from .models import Follow
# 此serializer只用来反序列化，全部默认为read_only

class ShortAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'  # 或者您可以列出需要的字段

class FollowSerializer(serializers.ModelSerializer):
    author = ShortAuthorSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['author']  # 或者您可以列出需要的字段