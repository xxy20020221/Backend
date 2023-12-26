from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Q, Subquery, OuterRef
from django.shortcuts import get_object_or_404

import os

from rest_framework import generics, viewsets, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Create your views here.
import Essay
from UserManage.models import User
from Analysis.models import Analysis
from Essay.models import Work
from Message.models import Message
from utils import *
from utils.tools import list_model_to_dict


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_analysis(request):
    # 创建解析，需要上传文件与其url
    # file = request.data.get('file')
    file = request.FILES.get('file')
    works = request.data.get('openalex_id')
    title_analysis = request.data.get('title_analysis')
    file_url = 'http://121.36.19.201/media/'
    # file_url += str(file)
    title = request.data.get('title', None)
    display_name = request.data.get('title', '')
    author_display_name = request.data.get('author_display_name', '')
    cited_by_count = request.data.get('cited_by_count', None)
    created_time = request.data.get('created_time', None)
    uid = request.user.id
    now_user = User.objects.get(id=uid)
    
    try:
        work = Work.objects.filter(open_alex_id=works)
        print(work)
        if not work.exists():
            work = Work.objects.create(
                open_alex_id=works,
                title=title,
                display_name=display_name,
                author_display_name=author_display_name,
                cited_by_count=cited_by_count,
                created_time=created_time
            )
        else:
            work = work.first()
        analysis = Analysis.objects.create(
            open_alex_id_work=works,
            works=work,
            file_url=file_url,
            file=file,
            title=title_analysis,
            user=User.objects.get(id=request.user.id)
        )
        analysis.file_url = analysis.file_url + str(analysis.file)
        analysis.save()
        administrators = User.objects.filter(is_staff=True)
        for user in administrators:
            try:
                Message.objects.create(
                    sender=now_user,
                    receiver=user,
                    type=6,
                    content="有解析需要被审核",
                    analysis=analysis,
                    work=work,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Analysis created successfully, sending to be examined", "id": analysis.id},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def examine_analysis(request):
    # 管理员进行解析的审核，flag为0为不通过，1为通过
    message_id = request.data.get('message_id')
    message = Message.objects.get(id=message_id)
    analysis = message.analysis
    flag = request.data.get('flag')
    flag = int(flag)
    if flag == 1:
        analysis.is_examined = True
        analysis.save()

    try:
        message1 = Message.objects.create(
            sender=User.objects.get(id=request.user.id),
            receiver=analysis.user,
            type=flag + 7,
            analysis=analysis,
        )
        if(flag):
            message1.content="您的解析审核已通过"
        else:
            message1.content="您的解析审核未通过"
        message1.save()

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    message.is_read = True
    message.save()
    return Response({"message": "Examination complete", "id": message1.id},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_analysis(request):
    # 获得一个论文页面的所有解析
    work = request.data.get('work_id')
    try:
        work_id = Work.objects.get(open_alex_id=work)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    title = request.query_params.get('title')
    created_time = request.query_params.get('created_time')
    created_before = request.query_params.get('created_before')
    created_after = request.query_params.get('created_after')

    query = Q(works=work_id) & Q(is_examined=True)
    if title:
        query &= Q(title__icontains=title)
    if created_time:
        query &= Q(created_time__date=created_time)
    if created_before:
        query &= Q(created_time__lt=created_before)
    if created_after:
        query &= Q(created_time__gt=created_after)

    try:
        analysis = Analysis.objects.filter(query)
        result = []
        for a in analysis:
            n = model_to_dict(a,exclude='file')
            n['username'] = a.user.username
            result.append(n)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_analysis_one(request):
    # 获取某个解析
    analysis_id = request.data.get('analysis_id')
    try:
        analysis = Analysis.objects.get(id=analysis_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(model_to_dict(analysis, exclude='file'), status=status.HTTP_200_OK)
