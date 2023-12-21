from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'Comment'

from .views import (
    comment_on_work,
    get_comment_on_work,
    comment_on_analysis,
    get_comment_on_analysis,
    comment_on_comment,
    get_comment_on_comment,
    remove_comments,

)

router = DefaultRouter()

urlpatterns = [
    path('comment_on_work/', comment_on_work, name='comment_on_work'),
    path('get_comment_on_work/<str:openalex_id>', get_comment_on_work, name='get_comment_on_work'),
    path('comment_on_analysis/', comment_on_analysis, name='comment_on_analysis'),
    path('get_comment_on_analysis/<str:analysis_id>', get_comment_on_analysis, name='get_comment_on_analysis'),
    path('comment_on_comment/', comment_on_comment, name='comment_on_comment'),
    path('get_comment_on_comment/<str:comment_id>', get_comment_on_comment, name='get_comment_on_comment'),
    path('remove_comments/<str:comment_id>', remove_comments, name='remove_comments'),

]+router.urls