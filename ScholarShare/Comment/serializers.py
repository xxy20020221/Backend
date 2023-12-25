from rest_framework import serializers

from datetime import datetime
from UserManage.models import User
import string
import os 
from .models import Comment,CommentToAnalysis,CommentToComment,CommentToWork
from Analysis.models import Analysis
# 此serializer只用来反序列化，全部默认为read_only

class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']  # 或者您可以列出需要的字段


class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    user = ShortUserSerializer(read_only=True)
    replied_user = ShortUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id','user','replied_user','type','level','created_time','content']

class CommentToWorkSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    user = ShortUserSerializer(read_only=True)
    replied_user = ShortUserSerializer(read_only=True)
    class Meta:
        model = CommentToWork
        fields = ['id','user','replied_user','type','level','created_time','content','work_openalex_id']


class ShortAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id']  # 或者您可以列出需要的字段 

      
class CommentToAnalysisSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    user = ShortUserSerializer(read_only=True)
    replied_user = ShortUserSerializer(read_only=True)
    analysis = ShortAnalysisSerializer(read_only=True)
    class Meta:
        model = CommentToAnalysis
        fields = ['id','user','replied_user','type','level','created_time','content','analysis']

class CommentToCommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    user = ShortUserSerializer(read_only=True)
    replied_user = ShortUserSerializer(read_only=True)
    analysis = ShortAnalysisSerializer(read_only=True)
    father = CommentSerializer(read_only=True)
    class Meta:
        model = CommentToComment
        fields = ['id','user','replied_user','type','level','created_time','content','analysis','work_openalex_id','father']