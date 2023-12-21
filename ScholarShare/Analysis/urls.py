from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'UserManage'


router = DefaultRouter()

urlpatterns = [
    path('analysis/create', views.create_analysis, name='create_analysis'),
    path('analysis/examine', views.examine_analysis, name='examine_analysis'),
    path('work/getana', views.get_analysis, name='get_analysis'),
    path('analysis/get', views.get_analysis_one, name='get_analysis_one')
]+router.urls