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
from utils.tools import list_model_to_dict
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMessages(request):
    # 获取所有消息，请求字段{type,sender_id,created_time,created_before,created_after}
    user_id = request.user.id

    type = request.query_params.get('type')
    
    sender_id = request.query_params.get('sender_id')
    created_time = request.query_params.get('created_time')
    created_before = request.query_params.get('created_before')
    created_after = request.query_params.get('created_after')
    is_read = request.query_params.get('is_read')

    query = Q(receiver_id=user_id)
    if type:
        query &= Q(type=type)
    if sender_id:
        query &= Q(sender_id=sender_id)
    if created_time:
        query &= Q(created_time__date=created_time)
    if created_before:
        query &= Q(created_time__lt=created_before)
    if created_after:
        query &= Q(created_time__gt=created_after)
    if is_read:
        query &= Q(is_read=bool(int(is_read)))

    try:
        messages = Message.objects.filter(query)
        needs = list_model_to_dict(messages, fields=['pdf'])
        results = []
        for i in range(messages.count()):
            n = needs[i]
            n['sender_name'] = messages[i].sender.username
            if messages[i].work is not None:
                n['work_title'] = messages[i].work.title
            if messages[i].analysis is not None:
                n['analysis_url'] = messages[i].analysis.file_url
            results.append(n)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(results, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeMessage(request):
    # 删除消息，请求字段{message_id}
    user_id = request.user.id
    message_id = request.data.get('message_id')
    
    if not message_id:
        Message.objects.filter(receiver_id=user_id).delete()
    else:
        Message.objects.filter(id=message_id).delete()

    return Response({"message": "success"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def readMessage(request):
    message_id = request.data.get('message_id')
    message = Message.objects.get(id=int(message_id))
    message.is_read = True
    message.save()
    return Response({"message": "已读"}, status=status.HTTP_200_OK)