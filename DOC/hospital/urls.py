from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from . import views
from .views import HospitalManagementView, HospitalProfileViewSet


# /hospital/
router = DefaultRouter()
router.register('hospital', views.HospitalManagementView, basename='hospital')
router.register(r'hospital-profile', HospitalProfileViewSet, basename='hospital-profile')




urlpatterns = [
    path('', include(router.urls)), 
    re_path(r'hospital/(?P<pk>\d+)/$', HospitalManagementView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='hospital-retrieve-update-destroy'),     
]