import requests
from django.forms import model_to_dict
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
import copy
from UserManage.models import History, User, AuthorName
from utils.tools import list_model_to_dict
#TODO 目前cache是保存所有信息，不知道会不会有缓存炸的情况，接下来要处理缓存里处理的信息缓解压力
def cache_get_value(type,params,per_page,pages):
    
    key = json.dumps(params)
    # value = None
    value = cache.get(key)
    base_url = "https://api.openalex.org"
    api_caller = APICaller(base_url)
    
    if value is None:
        print("cache not found, find via api")
        try:
            # 获取文章
            value = list(api_caller.get_all(type,params,per_page=int(per_page),pages=[int(pages)]))
            value = value[0]

            # 获取每个类型的数量  这个要增加很长的搜索时间，考虑展示的时候要不要优化掉
            if type=="works":
                params['group_by']='concepts.id'
                params['sort']='count:desc'
                concepts_type = api_caller.get(type,params)
                value['concepts_count'] = {}
                for i in range(len(concepts_type['group_by'])):
                    value['concepts_count'][concepts_type['group_by'][i]['key_display_name']] = concepts_type['group_by'][i]['count']
            
            # 处理abstract
            if type == "works":
                for i in range(len(value['results'])):
                    abstract_inverted_index = value['results'][i].get('abstract_inverted_index',None)
                    if(abstract_inverted_index is not None):
                        
                        tmp = convert_abstract(abstract_inverted_index)
                        value['results'][i]['abstract'] = tmp
                        value['results'][i]['abstract_inverted_index'] = None
        except:
            
            SystemError("OpenAlex error")
        if(value is not None):   
            cache.set(key,value)
    return value

def cache_get_value_not_paged(type,params):
    key = json.dumps(params)
    # value = None
    value = cache.get(key)
    base_url = "https://api.openalex.org"
    api_caller = APICaller(base_url)
    if value is None:
        print("cache not found, find via api")
        try:
            value = api_caller.get(type,params)

            # 处理abstract
            for i in range(len(value['results'])):
                abstract_inverted_index = value['results'][i].get('abstract_inverted_index',None)
                if(abstract_inverted_index is not None):
                    
                    tmp = convert_abstract(abstract_inverted_index)
                    value['results'][i]['abstract'] = tmp
                    value['results'][i]['abstract_inverted_index'] = None
        except:
            
            SystemError("OpenAlex error")
        if(value is not None):   
            cache.set(key,value)
    return value


def get_single_object(type:String,id):
    base_url = "https://api.openalex.org"
    api_caller = APICaller(base_url)
    params = {}
    # value = None
    value = cache.get(id)
    if value is None:
        try:
            value = api_caller.get(type+'/'+id,params)
            
            if type == "works":
                abstract_inverted_index = value.get('abstract_inverted_index',None)
                
                if(abstract_inverted_index is not None):
                    
                    tmp = convert_abstract(abstract_inverted_index)
                    value['abstract'] = tmp
                    value['abstract_inverted_index'] = None
        except:
            SystemError("OpenAlex error")

        

        if(value is not None):   
            cache.set(id,value)
    return value
    

# 获取所有openalex的文献数量
def get_open_alex_data_num():
    # 创建一个 OpenAlex 对象
    open_alex = OpenAlex("20351008@buaa.edu.cn")
    key = "open_alex_num"
    value = cache.get(key)
    # 如果缓存中没有
    if value is None:
        work_single = next(iter(open_alex.get_list_of_works(per_page=1)))
        work_count = work_single['meta']['count']
        author_single = next(iter(open_alex.get_list_of_authors(per_page=1)))
        author_count = author_single['meta']['count']
        venues_single = next(iter(open_alex.get_list_of_venues(per_page=1)))
        venues_count = venues_single['meta']['count']
        institutions_single = next(iter(open_alex.get_list_of_institutions(per_page=1)))
        institutions_count = institutions_single['meta']['count']
        concepts_single = next(iter(open_alex.get_list_of_concepts(per_page=1)))
        concepts_count = concepts_single['meta']['count']
        value = work_count, author_count, venues_count, institutions_count, concepts_count
        cache.set(key, value)
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

def convert_abstract(inverted_index):
    position_word_map = {}

    # 遍历倒排索引中的每个单词和它们的位置列表
    for word, positions in inverted_index.items():
        for position in positions:
            position_word_map[position] = word

    # 根据位置对单词进行排序
    sorted_positions = sorted(position_word_map.keys())

    # 使用排序后的单词位置重构文本
    reconstructed_text = ' '.join(position_word_map[pos] for pos in sorted_positions)


    return reconstructed_text




@api_view(['POST'])
@permission_classes([AllowAny])
def get_works(request):
    
    user_id = request.user.id
    params: dict = request.query_params
    params = convert_query_params(params)
    final_filter = params.get('filter')
    advanced = request.data.get('isAdvanced', None)
    single_object_id = request.data.get('single_object_id',None)
    isAutoComplete = params.get('isAutoComplete', None)
    group_by = params.get('group_by',None)
    concepts_level = request.data.get('concepts_level',None)
    base_url = "works"
    # add_history(params.get('search', None), user_id, 1, advanced)

    # if(group_by):
    #     if(group_by=="author_position"):

    
    if(isAutoComplete):
        base_url = "autocomplete/" + base_url

    if(single_object_id):
        value = get_single_object(base_url,single_object_id)
        if user_id is not None:
            name = value['authorships']
            names = ''
            tmp = []
            for n in name:
                names = names + n['author']['display_name'] + ','
                tmp.append(n['author']['display_name'])
            history = History.objects.create(
                user=request.user,
                title=value['title'],
                publication_date=value['publication_date'],
                language=value['language'],
                open_alex_id=single_object_id,
                cited_by_count=value['cited_by_count'],
                author_name=names
            )
            for t in tmp:
                AuthorName.objects.create(
                    history=history,
                    name=t
                )
        return Response(value, status=status.HTTP_201_CREATED)

    if advanced:
        # 遍历 final_filter 中的每个项目
        for item in final_filter.split(','):
            key, value = item.split(':')

            # 处理不同的属性
            if key == 'authorships.author.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("authors", search_param)
                ids = '|'.join([str(author['id']) for author in value_response['results']])
                final_filter = final_filter.replace(item, f"authorships.author.id:{ids}")

            elif key == 'authorships.institutions.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("institutions", search_param)
                ids = '|'.join([str(inst['id']) for inst in value_response['results']])
                final_filter = final_filter.replace(item, f"host_venue.id:{ids}")

            elif key == 'concepts.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("concepts", search_param)
                ids = '|'.join([str(concept['id']) for concept in value_response['results']])
                final_filter = final_filter.replace(item, f"concepts.id:{ids}")

            elif key == 'locations.source.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("sources", search_param)
                ids = '|'.join([str(concept['id']) for concept in value_response['results']])
                final_filter = final_filter.replace(item, f"locations.source.id:{ids}")

        params['filter'] = final_filter

    per_page = params.get('per_page', 25)
    pages = params.get('page', 1)
    value = cache_get_value(base_url, params, per_page, pages)
    if(concepts_level and group_by):
        
        tmp_params = {'filter':'level:'}
        tmp_params['filter']=tmp_params['filter']+concepts_level
        tmp_params['per_page']=300
        tmp_params['select']="display_name"

        filter_map = cache_get_value("concepts",params=tmp_params,pages=1,per_page=300)['results']
        
        for i in range(len(value['group_by'])):
            flag = 0
            name = value['group_by'][i].get('key_display_name')
            for x in filter_map:
                name2 = x.get('display_name')
                if(name==name2):
                    flag=1
                    break
            if not flag:
                value['group_by'][i]=None

        

    
    return Response(value, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
def get_authors(request):
    
    user_id = request.user.id
    params: dict = request.query_params
    params = convert_query_params(params)
    final_filter = params.get('filter')
    advanced = request.data.get('isAdvanced', None)
    single_object_id = request.data.get('single_object_id',None)
    base_url = "authors"
    # add_history(params.get('search', None), user_id, 2, advanced)

    if(single_object_id):
        value = get_single_object(base_url,single_object_id)
        return Response(value, status=status.HTTP_201_CREATED)

    if advanced:
        # 遍历 final_filter 中的每个项目
        for item in final_filter.split(','):
            key, value = item.split(':')

            # 处理不同的属性
            if key == 'last_known_institution.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("institutions", search_param)
                ids = '|'.join([str(inst['id']) for inst in value_response['results']])
                final_filter = final_filter.replace(item, f"last_known_institution.id:{ids}")

            elif key == 'x_concepts.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("concepts", search_param)
                ids = '|'.join([str(concept['id']) for concept in value_response['results']])
                final_filter = final_filter.replace(item, f"x_concepts.id:{ids}")

        params['filter'] = final_filter

    per_page = params.get('per_page', 25)
    pages = params.get('page', 1)
    value = cache_get_value(base_url, params, per_page, pages)
    return Response(value, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_institutions(request):
    user_id = request.user.id
    params: dict = request.query_params
    params = convert_query_params(params)
    final_filter = params.get('filter')
    advanced = request.data.get('isAdvanced', None)
    single_object_id = request.data.get('single_object_id',None)
    group_by = params.get('group_by',None)
    concepts_level = request.data.get('concepts_level',None)
    base_url = "institutions"
    # add_history(params.get('search', None), user_id, 3, advanced)

    if(single_object_id):
        value = get_single_object(base_url,single_object_id)
        return Response(value, status=status.HTTP_201_CREATED)

    if advanced:
        # 遍历 final_filter 中的每个项目
        for item in final_filter.split(','):
            key, value = item.split(':')

            if key == 'x_concepts.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("concepts", search_param)
                ids = '|'.join([str(concept['id']) for concept in value_response['results']])
                final_filter = final_filter.replace(item, f"x_concepts.id:{ids}")

        params['filter'] = final_filter

    per_page = params.get('per_page', 25)
    pages = params.get('page', 1)
    value = cache_get_value(base_url, params, per_page, pages)

    if(concepts_level and group_by):
        
        tmp_params = {'filter':'level:'}
        tmp_params['filter']=tmp_params['filter']+concepts_level
        tmp_params['per_page']=300
        tmp_params['select']="display_name"

        filter_map = cache_get_value("concepts",params=tmp_params,pages=1,per_page=300)['results']
        
        for i in range(len(value['group_by'])):
            flag = 0
            name = value['group_by'][i].get('key_display_name')
            for x in filter_map:
                name2 = x.get('display_name')
                if(name==name2):
                    flag=1
                    break
            if not flag:
                value['group_by'][i]=None
    return Response(value, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_concepts(request):
    
    user_id = request.user.id
    params: dict = request.query_params
    params = convert_query_params(params)
    final_filter = params.get('filter')
    advanced = request.data.get('isAdvanced', None)
    single_object_id = request.data.get('single_object_id',None)
    base_url = "concepts"
    # add_history(params.get('search', None), user_id, 4, advanced)

    if(single_object_id):
        value = get_single_object(base_url,single_object_id)
        return Response(value, status=status.HTTP_201_CREATED)

    if advanced:
        # 遍历 final_filter 中的每个项目
        for item in final_filter.split(','):
            key, value = item.split(':')

            # 处理不同的属性
            if key == 'ancestors.display_name':
                search_filter = f"display_name.search:{value}"
                search_param = {'filter': search_filter, 'select': "id"}
                value_response = cache_get_value_not_paged("ancestors", search_param)
                ids = '|'.join([str(ancestor['id']) for ancestor in value_response['results']])
                final_filter = final_filter.replace(item, f"ancestors.id:{ids}")

        params['filter'] = final_filter

    per_page = params.get('per_page', 25)
    pages = params.get('page', 1)
    value = cache_get_value(base_url, params, per_page, pages)
    return Response(value, status=status.HTTP_201_CREATED)


# 分析边
@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_edges(request):
    edges = {}
    params = {}
    base_url = "https://api.openalex.org"
    works = request.data.get('works',None)
    api_caller = APICaller(base_url)
    related_to = 'related_to:'
    referenced = 'referenced_by:'
    for work in works:
        work_id = work.get('id')
        related_prompt = related_to+work_id
        referenced_prompt = referenced+work_id
        params['filter'] = related_prompt+','+referenced_prompt
        
        value = api_caller.get("works",params)

    return Response(value, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def show_history(request):
    user_id = request.user.id
    histories = History.objects.filter(user=user_id)
    need = []
    for history in histories:
        names = AuthorName.objects.filter(history=history)
        history = model_to_dict(history)
        history['name'] = list_model_to_dict(names)
        need.append(history)
    return Response(need, status=status.HTTP_200_OK)