import requests
from django.http import JsonResponse
from properties import *
from diophila import OpenAlex
from diophila.endpoints import Works
from diophila.api_caller import APICaller
from django.core.cache import cache
# Create your views here.
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
import json
from rest_framework.response import Response
from rest_framework import generics,viewsets,permissions,status

#TODO 目前cache是保存所有信息，不知道会不会有缓存炸的情况，接下来要处理缓存里处理的信息缓解压力
def cache_get_value(type,params,per_page,pages):
    key = json.dumps(params)
    value = cache.get(key)
    base_url = "https://api.openalex.org"
    api_caller = APICaller(base_url)
    
    if value is None:
        print("cache not found, find via api")
        try:
            
            value = list(api_caller.get_all(type,params,per_page=int(per_page),pages=[int(pages)]))
        except:
            SystemError("OpenAlex error")
        if(value is not None):   
            cache.set(key,value)
    return value

# 转换查询参数
def convert_query_params(query_params):
    params = {}
    for key, value in query_params.items():
        # 将列表中的第一个元素转换为字符串，如果列表为空则设为 None
        if key in ['per_page', 'page']:
            value = int(value)
        params[key] = value if value else None

    return params


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_works(request):
    user_id = request.user.id
    params = request.query_params
    params = convert_query_params(params)
    per_page = params.get('per_page',None)
    pages = params.get('page',None)
    value = cache_get_value("works",params,per_page,pages)
    

    return Response(value, status=status.HTTP_201_CREATED)



