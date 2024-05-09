from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register('doctor', views.DoctorAppointmentManagementView, basename='doctor-appointment')
router.register('test', views.TestAppointmentManagementView, basename='test-appointment')
router.register('info-management', views.AppointmentInfoManagementView, basename='AppointmentInfoManagementView')


urlpatterns = [
    path('', include(router.urls)),
]