from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router=DefaultRouter()
router.register('specialist', views.SpecialistManagementView, basename='specialist')

urlpatterns = [
    path('', include(router.urls)),
]