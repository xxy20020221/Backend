from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'UserManage'


router = DefaultRouter()

urlpatterns = [
    path('message/', views.getMessages, name='getMessages'),
    path('message/remove', views.removeMessage, name='removeMessage'),
]+router.urls