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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_analysis(request, essay_id):
    # 创建解析，需要上传文件与其url
    # file = request.data.get('file')
    file_url = request.data.get('file_url')
    works = Work.objects.get(id=essay_id)

    try:
        collection_work = Analysis.objects.create(
            works=works,
            file_url=file_url
        )
        if works.author.is_professional == 1:
            user = User.objects.get(author=works.author)
            try:
                Message.objects.create(
                    works=works,
                    author=works.author,
                    receiver=user
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Analysis created successfully", "id": collection_work.id},
                        status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analysis(request, work_id):
    works = Work.objects.get(id=work_id)
    analysis = 
