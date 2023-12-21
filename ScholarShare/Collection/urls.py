from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'Collection'

from .views import (
    createCollectionPackage,
    renameCollectionPackage,
    deleteCollectionPackage,
    getCollectionPackage,
    createCollectionWork,
    createCollectionAnalysis,
    getCollectionPackageContents,
    removeCollectionItem,

)

router = DefaultRouter()

urlpatterns = [
    path('createCollectionPackage/', createCollectionPackage, name='createCollectionPackage'),
    path('renameCollectionPackage/', renameCollectionPackage, name='renameCollectionPackage'),
    path('deleteCollectionPackage/', deleteCollectionPackage, name='deleteCollectionPackage'),
    path('getCollectionPackage/', getCollectionPackage, name='getCollectionPackage'),
    path('createCollectionWork/', createCollectionWork, name='createCollectionWork'),
    path('createCollectionAnalysis/', createCollectionAnalysis, name='createCollectionAnalysis'),
    path('getCollectionPackageContents/<int:collection_package_id>', getCollectionPackageContents, name='getCollectionPackageContents'),
    path('removeCollectionItem/', removeCollectionItem, name='removeCollectionItem'),
]+router.urls