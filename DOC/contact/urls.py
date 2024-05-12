from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register("", views.ContactMessageViewSet, basename="contact-person-list")

urlpatterns = [
    path('contact-person-list/', include(router.urls)),
    path('', views.contact_view,name='contact')
]