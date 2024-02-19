from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /hospital/
router = DefaultRouter()
router.register('management', views.HospitalManagementView, basename='hospital')


urlpatterns = [
    path('', include(router.urls)),      
]