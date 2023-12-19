from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'Essay'

from .views import (
    get_works
)

router = DefaultRouter()

urlpatterns = [
    path('get_works/', get_works, name='get_works'),

]+router.urls