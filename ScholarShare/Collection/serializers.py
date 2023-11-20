from rest_framework import serializers
from .models import CollectionAnalysis,CollectionWork,ColletionPackage
from datetime import datetime
import string
import os 

# 此serializer只用来反序列化，全部默认为read_only


class CollectionPackageSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = ColletionPackage
        fields = ['id','name','created_time','sum']
        
class CollectionWorkSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = CollectionWork
        fields = ['work','collection_package','created_time']


class CollectionAnalysisSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = CollectionAnalysis
        fields = ['analysis','collection_package','created_time']