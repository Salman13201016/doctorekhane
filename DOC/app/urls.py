from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /profile/
router = DefaultRouter()
router.register('division', views.DivisionView, basename='division')
router.register('district', views.DistrictView, basename='district')
router.register('state', views.StateView, basename='state')


urlpatterns = [
    path('', include(router.urls)),      
]