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
def create_analysis(request, essay_id):
    # 创建解析，需要上传文件与其url
    # file = request.data.get('file')
    essay_id = int(essay_id)
    file_url = request.data.get('file_url')
    works = Work.objects.get(id=essay_id)
    title = request.data.get('title')

    try:
        analysis = Analysis.objects.create(
            works=works,
            file_url=file_url,
            title=title,
            user=request.user.id
        )
        if works.author.is_professional == 1:
            user = User.objects.get(id=1)  # 此处为管理员的id，将审核信息发送给管理员
            try:
                Message.objects.create(
                    receiver=user,
                    type=6,
                    content="有解析需要被审核",
                    analysis=analysis,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Analysis created successfully, sending to be examined", "id": analysis.id},
                        status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def examine_analysis(request, message_id):
    # 管理员进行解析的审核，flag为0为不通过，1为通过
    message_id = int(message_id)
    message = Message.objects.get(id=message_id)
    analysis = message.analysis
    flag = request.data.get('flag')
    if flag == 1:
        analysis.is_examined = True
        analysis.save()

    try:
        Message.objects.create(
            receiver=analysis.user,
            type=flag + 7,
            content=str,
            analysis=analysis,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Examination complete", "id": message.id},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analysis(request, work_id):
    # 获得一个论文页面的所有解析
    work_id = int(work_id)

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
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(list_model_to_dict(analysis, fields=['file_url', 'file']), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analysis_one(request, analysis_id):
    analysis_id = int(analysis_id)
    try:
        analysis = Analysis.objects.get(id=analysis_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(model_to_dict(analysis, exclude='file'), status=status.HTTP_200_OK)
