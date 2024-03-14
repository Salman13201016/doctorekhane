from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
# router.register('chamber', views.ChamberManagementView, basename='chamber')
# router.register('experience', views.ExperienceManagementView, basename='experience')
# router.register('doctor-service', views.DoctorServiceManagementView, basename='doctor_service')
router.register('management', views.DoctorManagementView, basename='doctor-management')
router.register('doctor-profile-list', views.DoctorProfileListView, basename='doctor-profile-list')
router.register('doctor-profile', views.DoctorProfileView, basename='doctor-profile')
router.register('doctor-filter-keys', views.DoctorFilterApi, basename='doctor-filter')

urlpatterns = [
    path('', include(router.urls)),
]