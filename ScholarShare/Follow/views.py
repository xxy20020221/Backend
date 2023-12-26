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
from .models import Follow
from Essay.models import Author
from .serializers import FollowSerializer
# 注意这里我们假设的是 关注的是作者，而不是用户
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_follow(request):
    # 关注某人
    user = request.user
    openalex_id = request.data.get('openalex_id',None)

    
    real_name = request.data.get('real_name',None)
    work_count = request.data.get('work_count',None)
    created_time = request.data.get('created_time',None)
    institution_display_name = request.data.get('institution_display_name',None)

    new_Author = Author.objects.filter(open_alex_id=openalex_id)
    if not new_Author.exists():
        new_Author = Author.objects.create(
            open_alex_id=openalex_id,
            real_name=real_name,
            work_count=work_count,
            institution_display_name=institution_display_name,
        )
    else:
        new_Author = new_Author.first()

    author_id = new_Author.id
    try:
        follow = Follow.objects.create(
            user=user,
            author=new_Author
        )
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"Follow complete"},status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_follow(request):
    # 获取关注列表
    user = request.user
    try:
        follows = Follow.objects.filter(user=user)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    return Response(FollowSerializer(follows,many=True).data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_follow(request):
    user = request.user
    author_id = request.data.get('author_id')
    try:
        author = Author.objects.filter(open_alex_id=author_id).first()
        follows = Follow.objects.filter(user=user,author=author).first()
        follows.delete()
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"Unfollow complete"},status=status.HTTP_201_CREATED)