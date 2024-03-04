from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /hospital/
router = DefaultRouter()
router.register('management', views.HospitalManagementView, basename='hospital')
router.register('ambulance', views.AmbulanceManagementView, basename='ambulance')
router.register('hospital-filter-keys', views.HospitalFilterApi, basename='hospital-filter')
router.register('ambulance-filter-keys', views.AmbulanceFilterApi, basename='ambulance-filter')


urlpatterns = [
    path('', include(router.urls)),      
]