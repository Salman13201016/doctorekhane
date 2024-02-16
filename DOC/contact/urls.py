from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()


urlpatterns = [
    path('', views.contact_view,name='contact')
]