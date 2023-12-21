#django stuff
from django.forms import model_to_dict
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
# Core
import time
from datetime import datetime
import string
import os
import shutil
# rest_framework
from rest_framework import generics,viewsets,permissions,status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated,AuthenticationFailed,PermissionDenied
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# serializers
from Essay.models import Author
from Message.models import Message
from .models import User
from .serializers import UserSerializer
# Create your views here.
class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)
        
        if user:
            token,created = Token.objects.get_or_create(user=user)
            # login(request, user)
            return Response({'token': token.key}, status=200)
        else:
            raise AuthenticationFailed("wrong username or password")
    
class UserLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({'User logged out successfully'},status=200)
        else:
            raise NotAuthenticated("You are not logged in")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getinfo(request):
    uid = request.data.get('uid')
    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(model_to_dict(user, exclude=['author', 'avatar']), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editinfo(request):
    uid = request.data.get('uid')
    phone_number = request.data.get('phone_number')
    gender = request.data.get('gender')
    description = request.data.get('description')
    email = request.data.get('email')
    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    user.phone_number = phone_number
    user.gender = gender
    user.email = email
    user.description = description
    return Response({"message": "Info edited"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadimage(request):
    uid = request.data.get('uid')
    avatar_url = request.data.get('avatar_url')
    try:
        file = request.FILES.get('image')
        user = User.objects.get(id=uid)
        user.avatar = file
        user.avatar_url = avatar_url
        user.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "upload success"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadconfirm(request):
    uid = request.data.get('uid')
    aid = request.data.get('aid')
    try:
        file = request.FILES.get('image')
        user = User.objects.get(id=uid)
        author = Author.objects.get(id=aid)
        administrators = User.objects.filter(is_staff=True)
        for administrator in administrators:
            Message.objects.create(
                sender=user,
                receiver=administrator,
                type=10,
                author=author,
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "upload success"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def examine(request):
    mid = request.data.get('mid')
    data = request.data.get('data')
    try:
        message = Message.objects.get(id=mid)
        if data == 1:
            message.receiver.author=message.author
            message.receiver.save
            Message.objects.create(
                receiver=message.receiver,
                type=0,
                content="申请通过",
            )
        else:
            Message.objects.create(
                receiver=message.receiver,
                type=1,
                content="申请不通过",
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "success"}, status=status.HTTP_201_CREATED)
