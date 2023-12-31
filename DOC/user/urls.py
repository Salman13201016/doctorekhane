from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /profile/
router = DefaultRouter()
router.register('profile', views.ProfileView, basename='profile')
router.register('management', views.UserManagementView, basename='user-management')
router.register('super-management', views.SuperUserManagementView, basename='super-user-management')
# router.register('changepassword', views.ChangeOwnPasswordView, basename='user-changeownpassword'),


urlpatterns = [
    path('', include(router.urls)),      
]