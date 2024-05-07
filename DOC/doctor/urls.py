from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
# router.register('chamber', views.ChamberManagementView, basename='chamber')
# router.register('experience', views.ExperienceManagementView, basename='experience')
router.register('doctor-services', views.DoctorServiceManagementView, basename='doctor_service')
router.register('management', views.DoctorManagementView, basename='doctor-management')
router.register('profile-list', views.DoctorProfileListView, basename='doctor-profile-list')
router.register('profile', views.DoctorProfileView, basename='doctor-profile')
router.register('doctor-filter-keys', views.DoctorFilterApi, basename='doctor-filter')
router.register('review', views.ReviewViewSet, basename='review')
urlpatterns = [
    path('', include(router.urls)),
    path('reviews/update_reviews/', views.ReviewViewSet.as_view({'post': 'update_reviews'}), name='update-reviews'),

]