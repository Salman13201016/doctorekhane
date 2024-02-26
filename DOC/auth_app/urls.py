from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView

# /auth/
router = DefaultRouter()
router.register('signup', views.UserRegistrationView, basename='signup')

urlpatterns = [
    path('', include(router.urls)),   
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('login/', views.CustomLoginView.as_view()),
    path('password-reset-otp/', views.SendOTPView.as_view()),
    path('verify-reset-otp/', views.VerifyOTPView.as_view()),
    path('change-password/', views.UpdatePasswordView.as_view()),
    path('signup-otp/', views.SendOTPViewReg.as_view()),
    path('verify-signup-otp/', views.VerifyOTPViewReg.as_view()),
    path('social/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('social/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
]