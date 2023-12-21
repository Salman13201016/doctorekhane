from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView

# /auth/
router = DefaultRouter()
router.register('signup', views.UserRegistraionView, basename='signup')

urlpatterns = [
    path('', include(router.urls)),   
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('login/', views.CustomLoginView.as_view()),
    path('password-reset/', PasswordResetView.as_view()),
    
    path('password-change/',
         PasswordChangeView.as_view()),
]