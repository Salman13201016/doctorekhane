from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /hospital/
router = DefaultRouter()
router.register('management', views.HospitalManagementView, basename='hospital')
router.register('test-management', views.TestManagementView, basename='test')
router.register('profile-list', views.HospitalProfileListView, basename='hospital-profile-list')
router.register('profile', views.HospitalProfileView, basename='hospital-profile')
router.register('ambulance', views.AmbulanceManagementView, basename='ambulance')
router.register('hospital-filter-keys', views.HospitalFilterApi, basename='hospital-filter')
router.register('ambulance-filter-keys', views.AmbulanceFilterApi, basename='ambulance-filter')
router.register('test-categories', views.CategoryListAPIView, basename='category-list')

urlpatterns = [
    path('', include(router.urls)),
]