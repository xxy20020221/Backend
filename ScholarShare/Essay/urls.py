from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'Essay'

from .views import (
    get_works,
    get_authors,
    get_concepts,
    get_institutions,
    analyze_edges,
    show_history,
    get_work_by_open,
    get_author_avatar
)

router = DefaultRouter()

urlpatterns = [
    path('get_works/', get_works, name='get_works'),
    path('get_authors/', get_authors, name='get_authors'),
    path('get_institutions/', get_institutions, name='get_institutions'),
    path('get_concepts/', get_concepts, name='get_concepts'),
    path('analyze_edges/', analyze_edges, name='analyze_edges'),
    path('history/', show_history, name='show_history'),
    path('get_workid/', get_work_by_open, name='get_workid'),
    path('get_author_avatar/', get_author_avatar, name='get_workid'),

]+router.urls