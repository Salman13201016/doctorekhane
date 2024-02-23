from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /profile/
router = DefaultRouter()
router.register('profile', views.ProfileView, basename='profile')
router.register('management', views.UserManagementView, basename='user-management')
router.register('super-management', views.SuperUserManagementView, basename='super-user-management')
router.register('donor', views.DonorListView, basename='donor'),
router.register('donor-filter-keys', views.DonorFilterApi, basename='donor-filter'),


urlpatterns = [
    path('', include(router.urls)),      
]