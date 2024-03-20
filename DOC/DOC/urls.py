"""
URL configuration for DOC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from .views import index,nearby_hospitals

urlpatterns = [
    path('', index, name="index"),
    path('api/nearby-hospitals/', nearby_hospitals, name="nearby_hospitals"),
    path('admin/', admin.site.urls),
    path('api/app/', include('app.urls')),
    path('api/auth-app/', include('auth_app.urls')),
    path('api/user/', include('user.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/doctor/', include('doctor.urls')),
    path('api/hospital/', include('hospital.urls')),
    path('api/appointment/', include('appointment.urls')),
    
    path('create-password/password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
