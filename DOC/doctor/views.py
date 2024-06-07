from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from app.models import ActionLog
# model
from .models import Doctor, DoctorService, Chamber, Experience, Review
from user.models import User
# serializer
from rest_framework import serializers
from .serializers import  DoctorProfileSerializer,DoctorProfileManagementSerializer,DoctorManagementSerializer, DoctorServiceSerializer, ChamberSerializer, ExperienceSerializer, ReviewSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator, IsDoctor

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

# Create your views here.

# class ChamberManagementView(viewsets.GenericViewSet):
#     permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
#     serializer_class = ChamberSerializer
#     queryset = Chamber.objects.all()

#     def get_object(self):
#         return self.request.user

#     def retrieve(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object())
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def partial_update(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ExperienceManagementView(viewsets.GenericViewSet):
#     permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
#     serializer_class = ExperienceSerializer
#     queryset = Experience.objects.all()

#     def get_object(self):
#         return self.request.user

#     def retrieve(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object())
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def partial_update(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorServiceManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
    serializer_class = DoctorServiceSerializer
    queryset = DoctorService.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorProfileView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsDoctor]
    serializer_class = DoctorProfileManagementSerializer
    queryset = User.objects.filter(role='doctor')
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
    @action(detail=False, methods=['DELETE'], url_path='delete-own-chamber/(?P<id>[^/.]+)')
    def delete_chamber(self, request, id=None):
        try:
            chamber = Chamber.objects.get(id=id,doctor=request.user.doctor)
            chamber.delete()  # Delete the chamber
            return Response({'message': 'Chamber deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Chamber.DoesNotExist:
            return Response({'message': 'Chamber not found.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['DELETE'], url_path='delete-own-experience/(?P<id>[^/.]+)')
    def delete_experience(self, request, id=None):
        try:
            experience = Experience.objects.get(id=id,doctor=request.user.doctor)
            experience.delete()  # Delete the chamber
            return Response({'message': 'Experience deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Experience.DoesNotExist:
            return Response({'message': 'Experience not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['DELETE'], url_path='delete-own-service/(?P<id>[^/.]+)')
    def delete_service(self, request, id=None, doctor_id = None):
        try:
            service = DoctorService.objects.get(id=id)
            doctor = request.user
            if service in doctor.services.all():
                doctor.services.remove(service)
            return Response({'message': 'Doctor Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except service.DoesNotExist:
            return Response({'message': 'Doctor Service not found.'}, status=status.HTTP_404_NOT_FOUND)



class DoctorManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorManagementSerializer
    queryset = Doctor.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'published': ["exact"],
    }
    search_fields = ['name',"address",'name_bn',"address_bn",'license_no','license_no_bn']
    ordering_fields = ['name','name_bn',"position"]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or  self.action=="get_doctor_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin" or user.is_staff:
            return Doctor.objects.filter(profile=False).order_by("position").distinct()
        else:
            # Non-admin user, show only published blog posts
            return Doctor.objects.filter(published=True,profile=False).order_by("position").distinct()
        
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created doctor {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update doctor doctor {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted doctor {instance.name}",
                timestamp=timezone.now()
            )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get-doctor-by-slug/(?P<slug>[-\w]+)')
    def get_doctor_by_slug(self, request, slug=None):
        try:
            doctor = Doctor.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['DELETE'], url_path='delete-chamber/(?P<id>[^/.]+)')
    def delete_chamber(self, request, id=None):
        try:
            chamber = Chamber.objects.get(id=id)
            if chamber.name:
                ActionLog.objects.create(
                    user=request.user,
                    action=f"{request.user.username} deleted {chamber.doctor.name} chamber {chamber.name}",
                    timestamp=timezone.now()
                )
            else:
                ActionLog.objects.create(
                    user=request.user,
                    action=f"{request.user.username} deleted doctor {chamber.hospital.name}",
                    timestamp=timezone.now()
                )
            chamber.delete()  # Delete the chamber
            return Response({'message': 'Chamber deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Chamber.DoesNotExist:
            return Response({'message': 'Chamber not found.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['DELETE'], url_path='delete-experience/(?P<id>[^/.]+)')
    def delete_experience(self, request, id=None):
        try:
            experience = Experience.objects.get(id=id)
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted {experience.doctor.name} experience",
                timestamp=timezone.now()
            )
            experience.delete()  # Delete the chamber
            return Response({'message': 'Experience deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Experience.DoesNotExist:
            return Response({'message': 'Experience not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['DELETE'], url_path='delete-service/(?P<doctor_id>[^/.]+)/(?P<id>[^/.]+)')
    def delete_service(self, request, id=None, doctor_id = None):
        try:
            service = DoctorService.objects.get(id=id)
            doctor = Doctor.objects.get(id=doctor_id)
            if service in doctor.services.all():
                doctor.services.remove(service)
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted {service.service_name} from {doctor.name} service",
                timestamp=timezone.now()
            )
            return Response({'message': 'Doctor Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except service.DoesNotExist:
            return Response({'message': 'Doctor Service not found.'}, status=status.HTTP_404_NOT_FOUND)
            
class DoctorFilterApi(viewsets.GenericViewSet):
    queryset = Doctor.objects.filter(profile=False,published = True)
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'published': ["exact"],
    }

    search_fields = ['name',"address",'name_bn',"address_bn",'chamber__hospital__name']
    ordering_fields = ['name','name_bn']

    def list(self, request):
        specialists_data = request.GET.get("specialists__id__in").split(",") if "specialists__id__in" in request.GET else list(Doctor.objects.filter(profile=False,published = True).values_list('specialists__id', flat=True).distinct())
        doctorservices_data = request.GET.get("services__id__in").split(",") if "services__id__in" in request.GET else list(Doctor.objects.filter(profile=False,published = True).values_list('services__id', flat=True).distinct())
        upazila_data = request.GET.get("location__id__in").split(",") if "location__id__in" in request.GET else list(Doctor.objects.filter(profile=False,published = True).values_list('location__id', flat=True).distinct())
        district_data = request.GET.get("location__district__id__in").split(",") if "location__district__id__in" in request.GET else list(Doctor.objects.filter(profile=False,published = True).values_list('location__district__id', flat=True).distinct())
        division_data = request.GET.get("location__district__division__id__in").split(",") if "location__district__division__id__in" in request.GET else list(Doctor.objects.filter(profile=False,published = True).values_list('location__district__division__id', flat=True).distinct())
        filter_specialists = list(
            Doctor.objects.filter(
                services__id__in = doctorservices_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                published = True
            ).values_list('specialists__id', 'specialists__specialist_name','specialists__specialist_name_bn').distinct()
        )
        filter_doctorservices = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                published = True
            ).values_list('services__id', 'services__service_name','services__service_name_bn').distinct()
        )
        filter_district = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                published = True
            ).values_list('location__district__id', 'location__district__district_name').distinct()
        )
        filter_division = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__district__id__in = district_data,
                location__id__in = upazila_data,
                published = True
            ).values_list('location__district__division__id', 'location__district__division__division_name').distinct()
        )
        
        filter_upazila = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                published = True
            ).values_list('location__id', 'location__upazila_name').distinct()
        )
        # Additional filters
        filter_keys = {
            "specialist_filters": [
                {
                    "id": item[0],
                    "specialist_name": item[1],
                    "specialist_name_bn": item[2],
                    "count": len(Doctor.objects.filter(specialists__id=item[0],published = True).distinct())
                } for item in filter_specialists
            ],
            "doctorservices_filter": [
                {
                    "id": item[0],
                    "services_name": item[1],
                    "services_name_bn": item[1],
                    "count": len(Doctor.objects.filter(services__id=item[0],published = True).distinct())
                } for item in filter_doctorservices
            ],
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name": division_name,
                "count": len(Doctor.objects.filter(location__district__division__id=division_id,published = True).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name = district_item
                # Check if the district belongs to the current division
                if Doctor.objects.filter(location__district__id=district_id, location__district__division__id=division_id,published = True).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "count": len(Doctor.objects.filter(location__district__id=district_id,published = True).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name = upazila_item
                        # Check if the upazila belongs to the current district
                        if Doctor.objects.filter(location__id=upazila_id, location__district__id=district_id,published = True).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "count": len(Doctor.objects.filter(location__id=upazila_id,published = True).distinct())
                            }
                            
                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)
    

class DoctorProfileListView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorManagementSerializer
    queryset = Doctor.objects.filter(profile=True).distinct()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
    }
    search_fields = ["user__first_name","user__last_name","user__email","address","license_no"]
    ordering_fields = ['user__first_name']
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True, context={"request":request})
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewViewSet(viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsModerator]
    queryset =Review.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'published': ["exact"], 
        'user': ["exact"], 
        'doctor': ["exact"], 
        'hospital': ["exact"], 
        'rating': ["exact"], 
        'created_at': ["range"],
    }
    search_fields = ['user__first_name']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action == "partial_update":
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.all()

        # Filter based on user role
        if not (user.is_authenticated and (user.role == "admin" or user.is_staff)):
            # Non-admin users should only see published reviews
            queryset = queryset.filter(published=True)
        
        # Custom filter based on the role query parameter
        role = self.request.query_params.get('role', None)
        if role == 'doctor':
            queryset = queryset.filter(doctor__isnull=False)
        elif role == 'hospital':
            queryset = queryset.filter(hospital__isnull=False)

        return queryset.order_by("-id")
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        old_publish_status = instance.published

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()

            # Check if 'published' field has been updated
            if instance.published != old_publish_status:
                # Log action for change in published status
                ActionLog.objects.create(
                    user=request.user,
                    action=f"{request.user.username} {'published' if instance.published else 'unpublished'} a '{instance.user}' review",
                    timestamp=timezone.now()
                )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({'status':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
