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
from utils.tools import list_model_to_dict
from Comment.models import *
from Message.models import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_work(request, work_id):
    # 在论文下面评论
    work_id = int(work_id)
    content = request.data.get('data')
    try:
        comment = CommentToWork.objects.create(
            work=work_id,
            content=content,
            user=request.user.id
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    work = Work.objects.get(id=work_id)
    try:
        user = User.objects.get(author__work=work)
    except Exception as e:
        return Response({"message": "Comment complete", "id": comment.id},
                        status=status.HTTP_201_CREATED)
    try:
        Message.objects.create(
            receiver=user,
            sender=request.user.id,
            type=4,
            content=content,
            work=work_id,
        )
        user.unread_message_count += 1
        user.update()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Comment complete", "id": comment.id},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment_on_work(request, work_id):
    # 获取论文下的评论
    work_id = int(work_id)
    try:
        comments = CommentToWork.objects.filter(work=work_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(list_model_to_dict(comments), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_analysis(request, analysis_id):
    # 在解析下面评论
    work_id = int(analysis_id)
    content = request.data.get('data')
    analysis = Analysis.objects.get(works=work_id)
    try:
        comment = CommentToAnalysis.objects.create(
            analysis=work_id,
            content=content,
            user=request.user.id,
            type=1
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        Message.objects.create(
            receiver=analysis.user,
            sender=request.user.id,
            type=9,
            content=content,
            analysis=analysis
        )
        analysis.user.unread_message_count += 1
        analysis.user.update()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Comment complete", "id": comment.id},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment_on_analysis(request, analysis_id):
    # 获取论文下的评论
    work_id = int(analysis_id)
    try:
        comments = CommentToAnalysis.objects.filter(analysis=work_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(list_model_to_dict(comments), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_comment(request, comment_id):
    # 在评论下面评论
    comment_id = int(comment_id)
    content = request.data.get('data')
    comment = Comment.objects.get(id=comment_id)
    try:
        comment = CommentToComment.objects.create(
            father=comment,
            content=content,
            user=request.user.id,
            type=2
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        Message.objects.create(
            receiver=comment.user,
            sender=request.user.id,
            type=2,
            content=comment.content,
            reply=content
        )
        comment.user.unread_message_count += 1
        comment.user.update()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Comment complete", "id": comment.id},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment_on_comment(request, comment_id):
    # 获取评论下的评论
    comment_id = int(comment_id)
    try:
        comments = CommentToComment.objects.filter(father=comment_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(list_model_to_dict(comments), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove_comments(request, comment_id):
    comment_id = int(comment_id)
    try:
        Comment.objects.get(id=comment_id).delete()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Comment complete", },
                    status=status.HTTP_200_OK)
