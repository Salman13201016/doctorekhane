from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

# model
from .models import Specialist, Doctor, DoctorService, Chamber, Experience
# serializer
from rest_framework import serializers
from .serializers import  SpecialistSerializer, DoctorSerializer, DoctorServiceSerializer, ChamberSerializer, ExperienceSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator, IsDoctor

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class SpecialistManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialistSerializer
    queryset = Specialist.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ['specialist_name']
    ordering_fields = ['specialist_name']

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = []
        return super().get_permissions()
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

class ChamberManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()

    def get_object(self):
        return self.request.user

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExperienceManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()

    def get_object(self):
        return self.request.user

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorServiceManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
    serializer_class = DoctorServiceSerializer
    queryset = DoctorService.objects.all()

    def get_object(self):
        return self.request.user

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DoctorManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        'specialists__specialist_name': ['in'],
        'location__upazila__district__district_name': ['in'],
        'location__upazila__district__division__division_name': ['in'],
    }
    search_fields = ['name']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or  self.action=="get_doctor_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        requested_user = self.get_object()
        if requested_user.profile.role=="admin":
            raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
        requested_user.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    @action(detail=False, methods=['GET'], url_path='get-doctor-by-slug/(?P<slug>[-\w]+)')
    def get_doctor_by_slug(self, request, slug=None):
        try:
            doctor = Doctor.objects.get(slug=slug)
            serializer = self.get_serializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
