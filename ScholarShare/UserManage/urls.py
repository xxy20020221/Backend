from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'UserManage'

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,

)

router = DefaultRouter()

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('info/', views.getinfo, name='information'),
    path('editinfo/', views.editinfo, name='getInformation'),
    path('uploadconfirm/', views.uploadconfirm, name='uploadConfirm'),
    path('uploadimage/', views.uploadimage, name='uploadImage'),
    path('downloadimage/', views.downloadimage, name='uploadImage'),
    path('examine/', views.examine, name='examine'),
]+router.urls