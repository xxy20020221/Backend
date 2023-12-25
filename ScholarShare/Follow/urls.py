from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'Essay'

from .views import (
    create_follow,
    get_follow,
    revoke_follow,
)

router = DefaultRouter()

urlpatterns = [
    path('create_follow/',create_follow,name='create_follow'),
    path('get_follow/',get_follow,name="get_follow"),
    path('revoke_follow/',revoke_follow,name="revoke_follow"),

]+router.urls