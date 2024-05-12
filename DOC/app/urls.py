from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /profile/
router = DefaultRouter()
router.register('specialist', views.SpecialistManagementView, basename='specialist')
router.register('services', views.ServicesManagementView, basename='services')
router.register('team-member', views.TeamManagementView, basename='team-member')
router.register('site-settings', views.SiteSettingsManagementView, basename='site-settings')
router.register('landing-page-report', views.LandingPageReportView, basename='landing_page_report')
router.register('statistic-report', views.StatisticsViewSet, basename='statistic_report')
router.register('notice-management', views.NoticeManagementView, basename='notice')
router.register('goal-management', views.GoalManagementView, basename='goal')
router.register('others-content', views.OthersContentManagementView, basename='others-content')

urlpatterns = [
    path('', include(router.urls)),
    path('division/', views.DivisionListAPIView.as_view(), name='division-list'),
    path('districts/<int:division_id>/', views.DistrictListAPIView.as_view(), name='district-list'),
    path('upazilas/<int:district_id>/', views.UpazilaListAPIView.as_view(), name='upazila-list'),
    path('unions/<str:upazila_id>/', views.UnionListAPIView.as_view(), name='Unions-list'), 
    path('action-log/', views.ActionLogList.as_view(), name='action-log'),
    path('notifications/', views.NotificationAPI.as_view(), name='notification-list'),

]