# django stuff
from django.forms import model_to_dict
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
# Core
import time
from datetime import datetime
import string
import os
import shutil
# rest_framework
from rest_framework import generics, viewsets, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
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
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key

                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            # login(request, user)
            return Response({'token': token.key}, status=200)
        else:
            raise AuthenticationFailed("wrong username or password")


class UserLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({'User logged out successfully'}, status=200)
        else:
            raise NotAuthenticated("You are not logged in")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getinfo(request):
    uid = request.user.id
    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(model_to_dict(user, exclude=['author', 'avatar','true_man']), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editinfo(request):
    uid = request.user.id
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
    uid = request.user.id
    # print(request.FILES)
    # avatar_url = request.data.get('avatar_url')
    file = request.FILES.get('image')
    try:
        user = User.objects.get(id=uid)
        user.avatar = file
        user.save()
        user.avatar_url = 'http://121.36.19.201/media/' + str(user.avatar)
        user.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "upload success"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadimage(request):
    uid = request.user.id
    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"url": user.avatar_url}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadconfirm(request):
    uid = request.user.id
    try:
        image = request.FILES.get('image')
        file = request.FILES.get('pdf')
        openalex_id = request.data.get('openalex_id', None)

        real_name = request.data.get('real_name', None)
        work_count = request.data.get('work_count', None)
        created_time = request.data.get('created_time', None)
        institution_display_name = request.data.get('institution_display_name', None)
        user = User.objects.get(id=uid)
        user.true_man = image
        user.save()
        user.true_man_url = 'http://121.36.19.201/media/' + str(user.true_man)
        user.save()
        author = Author.objects.filter(open_alex_id=openalex_id)
        if not author.exists():
            author = Author.objects.create(
                open_alex_id=openalex_id,
                real_name=real_name,
                work_count=work_count,
                institution_display_name=institution_display_name,
                created_time=created_time
            )
        else:
            author=author.first()
        administrators = User.objects.filter(is_staff=True)
        for administrator in administrators:
            message = Message.objects.create(
                sender=user,
                receiver=administrator,
                pdf=file,
                type=10,
                author=author,
                url='http://121.36.19.201/media/'
            )
            message.url = message.url + str(message.pdf)
            message.save()
            user.is_professional = 0
            user.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "upload success"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadconfirm(request):
    mid = request.data.get('mid')
    try:
        message = Message.objects.get(id=mid)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"url": message.url}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def examine(request):
    mid = request.data.get('mid')
    data = request.data.get('data')
    try:
        message = Message.objects.get(id=mid)
        print(data)
        data=int(data)
        if data == 1:
            print("yes")
            message.sender.author = message.author
            message.sender.is_professional = 1
            message.sender.save()
            Message.objects.create(
                receiver=message.sender,
                sender=User.objects.get(id=request.user.id),
                type=0,
                content="您的认证申请已通过",
            )
        else:
            message.sender.is_professional = -1
            message.sender.save()
            Message.objects.create(
                receiver=message.sender,
                sender=User.objects.get(id=request.user.id),
                type=1,
                content="您的认证申请不通过",
            )
        message.is_read = True
        message.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "success"}, status=status.HTTP_201_CREATED)
