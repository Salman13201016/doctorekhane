from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('blog-management', views.BlogManagementView, basename='blog')
router.register('personal-blog-management', views.PersonalBlogManagementView, basename='personal-blog')
urlpatterns = [
    path('', include(router.urls)),
    
]