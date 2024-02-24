from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

# model
from .models import Doctor, DoctorService, Chamber, Experience
# serializer
from rest_framework import serializers
from .serializers import  DoctorSerializer, DoctorServiceSerializer, ChamberSerializer, ExperienceSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator, IsDoctor

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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

# class DoctorServiceManagementView(viewsets.GenericViewSet):
#     permission_classes = [IsDoctor,IsModerator,IsSuperAdmin]
#     serializer_class = DoctorServiceSerializer
#     queryset = DoctorService.objects.all()

#     def get_object(self):
#         return self.request.user

#     def retrieve(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object())
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def partial_update(self, request, pk=None):
#         serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True,)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DoctorManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
    }
    search_fields = ['name',"address"]
    ordering_fields = ['name']


    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or  self.action=="get_doctor_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
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
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True, context={"request":request})
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

class DoctorFilterApi(viewsets.GenericViewSet):
    queryset = Doctor.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
    }

    search_fields = ['name',"address",'chamber__hospital__name']
    ordering_fields = ['name']

    def list(self, request):
        specialists_data = request.GET.get("specialists__id__in").split(",") if "specialists__id__in" in request.GET else list(Doctor.objects.all().values_list('specialists__id', flat=True).distinct())
        doctorservices_data = request.GET.get("services__id__in").split(",") if "services__id__in" in request.GET else list(Doctor.objects.all().values_list('services__id', flat=True).distinct())
        union_data = request.GET.get("location__union_name__in").split(",") if "location__union_name__in" in request.GET else list(Doctor.objects.all().values_list('location__union_name', flat=True).distinct())
        upazila_data = request.GET.get("location__upazila__id__in").split(",") if "location__upazila__id__in" in request.GET else list(Doctor.objects.all().values_list('location__upazila__id', flat=True).distinct())
        district_data = request.GET.get("location__upazila__district__id__in").split(",") if "location__upazila__district__id__in" in request.GET else list(Doctor.objects.all().values_list('location__upazila__district__id', flat=True).distinct())
        division_data = request.GET.get("location__upazila__district__division__id__in").split(",") if "location__upazila__district__division__id__in" in request.GET else list(Doctor.objects.all().values_list('location__upazila__district__division__id', flat=True).distinct())
        filter_specialists = list(
            Doctor.objects.filter(
                services__id__in = doctorservices_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('specialists__id', 'specialists__specialist_name').distinct()
        )
        filter_doctorservices = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('services__id', 'services__service_name').distinct()
        )
        filter_district = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('location__upazila__district__id', 'location__upazila__district__district_name').distinct()
        )
        filter_division = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('location__upazila__district__division__id', 'location__upazila__district__division__division_name').distinct()
        )
        filter_union = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__upazila__district__division__id__in = division_data,
            ).values_list('location__union_name','location__upazila__id','location__upazila__district__id','location__upazila__district__division__id').distinct()
        )
        filter_upazila = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = doctorservices_data,
                location__upazila__district__id__in = district_data,
                location__union_name__in = union_data,
                location__upazila__district__division__id__in = division_data,
            ).values_list('location__upazila__id', 'location__upazila__upazila_name').distinct()
        )
        # Additional filters
        filter_keys = {
            "specialist_filters": [
                {
                    "id": item[0],
                    "specialist_name": item[1],
                    "count": len(Doctor.objects.filter(specialists__id=item[0]).distinct())
                } for item in filter_specialists
            ],
            "doctorservices_filter": [
                {
                    "id": item[0],
                    "services_name": item[1],
                    "count": len(Doctor.objects.filter(services__id=item[0]).distinct())
                } for item in filter_doctorservices
            ],
            "division_filters": [
                {
                    "id": item[0],
                    "division_name": item[1],
                    "count": len(Doctor.objects.filter(location__upazila__district__division__id=item[0]).distinct())
                } for item in filter_division
            ],
            "district_filter": [
                {
                    "id": item[0],
                    "district_name": item[1],
                    "count": len(Doctor.objects.filter(location__upazila__district__id=item[0]).distinct())
                } for item in filter_district
            ],
            "upazila_filter": [
                {
                    "id": item[0],
                    "upazila_name": item[1],
                    "count": len(Doctor.objects.filter(location__upazila__id=item[0]).distinct())
                } for item in filter_upazila
            ],
            "union_filter": [
                {
                    "union_name": item[0],
                    "union_count": len(Doctor.objects.filter(location__union_name=item[0]).distinct()),
                    "upazila_name": item[1],
                    "upazila_count": len(Doctor.objects.filter(location__upazila__id=item[1]).distinct()),
                    "district_name": item[2],
                    "district_count": len(Doctor.objects.filter(location__upazila__district__id=item[2]).distinct()),
                    "division_name": item[3],
                    "division_count": len(Doctor.objects.filter(location__upazila__district__division__id=item[3]).distinct())
                } for item in filter_union
            ]
        }

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)