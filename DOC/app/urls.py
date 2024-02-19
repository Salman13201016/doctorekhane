from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /profile/
router = DefaultRouter()
router.register('specialist', views.SpecialistManagementView, basename='specialist')
router.register('services', views.ServicesManagementView, basename='services')
urlpatterns = [
    path('', include(router.urls)),
    path('division/', views.DivisionListAPIView.as_view(), name='division-list'),
    path('districts/<int:division_id>/', views.DistrictListAPIView.as_view(), name='district-list'),
    path('upazilas/<int:district_id>/', views.UpazilaListAPIView.as_view(), name='upazila-list'),
    path('unions/<str:upazila_id>/', views.UnionListAPIView.as_view(), name='Unions-list'), 
]