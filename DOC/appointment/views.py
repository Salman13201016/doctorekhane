from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

# model
from .models import DoctorAppointment, TestAppointment
from user.models import User
# serializer
from rest_framework import serializers
from .serializers import  DoctorAppointmentManagementSerializer, TestAppointmentManagementSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator,IsDoctor

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
# Create your views here.
class DoctorAppointmentManagementView(viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = DoctorAppointmentManagementSerializer
    queryset = DoctorAppointment.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        'patientstatus': ['exact'],
        'date': ['range'],
        'time': ['range'],
    }
    search_fields = ['appointment_id',"user__first_name","user__last_name","doctor__name"]
    ordering_fields = ['id']

    
    def retrieve(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            # Assuming the user's ID is linked to the instance (for example, in user field)
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():  # Check if queryset is empty
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.role == 'doctor':
            queryset = DoctorAppointment.objects.filter(doctor__user=request.user)
        elif request.user.role == 'general':
            queryset = DoctorAppointment.objects.filter(user=request.user)
        else:
            queryset = DoctorAppointment.objects.all()
        
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists(): 
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)    

class TestAppointmentManagementView(viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = TestAppointmentManagementSerializer
    queryset = TestAppointment.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        'private': ['exact'],
        'date': ['range'],
        'time': ['range'],
    }
    search_fields = ['appointment_id',"user__first_name","user__last_name","test__test_name"]
    ordering_fields = ['id']

    
    def retrieve(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            # Assuming the user's ID is linked to the instance (for example, in user field)
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():  # Check if queryset is empty
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.role == 'hospital':
            queryset = TestAppointment.objects.filter(hospital__user=request.user)
        elif request.user.role == 'general':
            queryset = TestAppointment.objects.filter(user=request.user)
        else:
            queryset = TestAppointment.objects.all()
        
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists(): 
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)    
