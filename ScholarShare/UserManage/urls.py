from rest_framework.routers import DefaultRouter
from django.urls import path

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
]+router.urls