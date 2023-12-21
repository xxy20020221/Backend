from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F,Q,Subquery,OuterRef
from django.shortcuts import get_object_or_404

import os

from rest_framework import generics,viewsets,permissions,status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated,AuthenticationFailed,PermissionDenied
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Create your views here.
from .models import CollectionAnalysis,CollectionWork,ColletionPackage
from Essay.models import Work
from Analysis.models import Analysis
from .serializers import CollectionPackageSerializer,CollectionAnalysisSerializer,CollectionWorkSerializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCollectionPackage(request):
    # 添加文件夹，创建字段{name}
    user_id = request.user.id
    name = request.data.get('name')

    if ColletionPackage.objects.filter(user_id=user_id, name=name).exists():
        return JsonResponse({'error': 'A CollectionPackage with this name already exists'}, status=400)
    try:
        addCollectionPackage = ColletionPackage.objects.create(user_id=user_id,name=name)
        return Response({"message": "CollectionPackage created successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def renameCollectionPackage(request):
    # 重命名文件夹，需要字段{collection_package_id,new_name}
    collection_package_id = request.data.get('collection_package_id')
    new_name = request.data.get('new_name')

    if not collection_package_id or not new_name:
        return Response({"error": "collection_package_id and new_name are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        collection_package = ColletionPackage.objects.get(id=collection_package_id)
        collection_package.name = new_name
        collection_package.save()
        return Response({"message": "CollectionPackage renamed successfully"}, status=status.HTTP_200_OK)
    except ColletionPackage.DoesNotExist:
        return Response({"error": "CollectionPackage not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteCollectionPackage(request):
    # 删除文件夹，需要字段{collection_package_id}
    collection_package_id = request.data.get('collection_package_id')
    

    if not collection_package_id:
        return Response({"error": "collection_package_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        collection_package = ColletionPackage.objects.get(id=collection_package_id)
        collection_package.delete()
        return Response({"message": "CollectionPackage deleted successfully"}, status=status.HTTP_200_OK)
    except ColletionPackage.DoesNotExist:
        return Response({"error": "CollectionPackage not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCollectionPackage(request):
    # 获取文件夹，查询条件{null,name,created_time,created_before,created_after}，查询返回字段{id,name,created_time,sum}
    user_id = request.user.id
    name = request.query_params.get('name')
    created_time = request.query_params.get('created_time')
    created_before = request.query_params.get('created_before')
    created_after = request.query_params.get('created_after')

    query = Q(user_id=user_id)
    if name:
        query &= Q(name__icontains=name)
    if created_time:
        query &= Q(created_time__date=created_time)
    if created_before:
        query &= Q(created_time__lt=created_before)
    if created_after:
        query &= Q(created_time__gt=created_after)

    try:
        collectionPackage = ColletionPackage.objects.filter(query)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    return Response(CollectionPackageSerializer(collectionPackage,many=True).data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCollectionWork(request):
    # 文件夹下创建work,默认work和收藏夹必存在,创建字段{work_id,collection_package_id}
    openalex_id = request.data.get('openalex_id')
    collection_package_id = request.data.get('collection_package_id')

    # work的属性，这里需要前端传给后端信息，减少检索时间
    title = request.data.get('title',None)
    display_name = request.data.get('title','')
    author_display_name = request.data.get('author_display_name','')
    cited_by_count = request.data.get('cited_by_count',None)
    created_time = request.data.get('created_time',None)

    new_work = Work.objects.filter(open_alex_id=openalex_id)

    if not new_work.exists():

        new_work = Work.objects.create(
            open_alex_id=openalex_id,
            title=title,
            display_name=display_name,
            author_display_name=author_display_name,
            cited_by_count=cited_by_count,
            created_time=created_time
        )[0]
    else:
        new_work = new_work.first()

    # 获取新创建的对象的ID
    work_id = new_work.id


    collection_package = ColletionPackage.objects.get(id=collection_package_id)
    
    if CollectionWork.objects.filter(work_id=work_id, collection_package_id=collection_package_id).exists():
        return Response({"error": "Work already in the CollectionPackage"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    try:
        collection_work = CollectionWork.objects.create(
            work_id=work_id,
            collection_package_id=collection_package_id
        )
        collection_package.sum+=1
        collection_package.save()
        return Response({"message": "CollectionWork created successfully", "id": collection_work.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCollectionAnalysis(request):
    # 文件夹下创建analysis,默认analysis和收藏夹必存在,创建字段{analysis_id,collection_package_id}
    analysis_id = request.data.get('analysis_id')
    collection_package_id = request.data.get('collection_package_id')
    collection_package = ColletionPackage.objects.get(id=collection_package_id)

    if CollectionAnalysis.objects.filter(analysis_id=analysis_id, collection_package_id=collection_package_id).exists():
        return Response({"error": "Analysis already in the CollectionPackage"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        collection_analysis = CollectionAnalysis.objects.create(
            analysis_id=analysis_id,
            collection_package_id=collection_package_id
        )
        collection_package.sum+=1
        collection_package.save()
        return Response({"message": "CollectionAnalysis created successfully", "id": collection_analysis.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCollectionPackageContents(request, collection_package_id):
    # 获取文件夹下的内容，查询条件{collection_package_id}，查询返回字段{works,analysis}
    try:
        
        collection_package = ColletionPackage.objects.get(id=collection_package_id)
   
        works = CollectionWork.objects.filter(collection_package=collection_package)
        analysis = CollectionAnalysis.objects.filter(collection_package=collection_package)

        
        work_serializer = CollectionWorkSerializer(works, many=True)
        
        analysis_serializer = CollectionAnalysisSerializer(analysis, many=True)
        
        response_data = {
            'works': work_serializer.data,
            'analysis': analysis_serializer.data
        }
        return Response(response_data)
    except ColletionPackage.DoesNotExist:
        return Response({'error': 'CollectionPackage not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeCollectionItem(request):
    # 删除文件夹下的内容，查询条件{work_id,analysis_id,collection_package_id}
    work_id = request.data.get('work_id')
    analysis_id = request.data.get('analysis_id')
    collection_package_id = request.data.get('collection_package_id')

    if work_id:
        CollectionWork.objects.filter(work_id=work_id, collection_package_id=collection_package_id).delete()
        return Response({"message": "Work removed from collection successfully"}, status=status.HTTP_200_OK)
    
    elif analysis_id:
        CollectionAnalysis.objects.filter(analysis_id=analysis_id, collection_package_id=collection_package_id).delete()
        return Response({"message": "Analysis removed from collection successfully"}, status=status.HTTP_200_OK)

    else:
        return Response({"error": "Invalid request, work_id or analysis_id required"}, status=status.HTTP_400_BAD_REQUEST)
    



    