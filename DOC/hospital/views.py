from datetime import datetime
from django.shortcuts import render
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# filter search sort
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.models import ActionLog
from .models import Hospital,Ambulance, HospitalService,Test, TestCatagory
from user.models import User
from .serializers import AmbulanceProfileManagementSerializer, HospitalProfileManagementSerializer,HospitalManagementSerializer,AmbulanceListSerializer,AmbulanceManagementSerializer, HospitalServiceSerializer, TestCatagorySerializer,TestSerializer
# pagination
from rest_framework.pagination import  LimitOffsetPagination
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsAmbulance, IsSuperAdmin,IsHospital,IsModerator
from django.db.models import Q
from django.utils import timezone

# Create your views here.

class HospitalServiceManagementView(viewsets.GenericViewSet):
    permission_classes = [IsHospital,IsModerator,IsSuperAdmin]
    serializer_class = HospitalServiceSerializer
    queryset = HospitalService.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListAPIView(viewsets.GenericViewSet):
    queryset = TestCatagory.objects.all()
    serializer_class = TestCatagorySerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by("-id")
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = TestSerializer
    queryset = Test.objects.filter(deleted=False).distinct().order_by("-id")
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'catagory__id': ['in'],
        'published': ["exact"],

    }
    
    search_fields = ['test_name','test_name_bn']
    ordering_fields = ['test_name','test_name_bn',"fee","fee_bn","position"]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action=="get_test_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin" or user.is_staff:
            return Test.objects.filter(deleted=False).order_by("position").distinct()
        else:
            # Non-admin user, show only published blog posts
            return Test.objects.filter(published=True,deleted=False).order_by("position").distinct()
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created test {instance.test_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update test {instance.test_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action=f"{request.user.username} deleted test {instance.test_name}",
            timestamp=timezone.now()
        )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['GET'], url_path='get-test-by-slug/(?P<slug>[-\w]+)')
    def get_test_by_slug(self, request, slug=None):
        try:
            test = Test.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({'message': 'Test not found.'}, status=status.HTTP_404_NOT_FOUND)

class HospitalProfileView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsHospital]
    serializer_class = HospitalProfileManagementSerializer
    queryset = User.objects.filter(role='hospital')
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
    
    @action(detail=False, methods=['DELETE'], url_path='delete-own-service/(?P<id>[^/.]+)')
    def delete_service(self, request, id=None, hospital_id = None):
        try:
            service = HospitalService.objects.get(id=id)
            hospital = request.user
            if service in hospital.services.all():
                hospital.services.remove(service)
            return Response({'message': 'Hospital Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except service.DoesNotExist:
            return Response({'message': 'Hospital Service not found.'}, status=status.HTTP_404_NOT_FOUND)
  

class HospitalManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsHospital]
    serializer_class = HospitalManagementSerializer
    queryset = Hospital.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'tests__id': ['in'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'category': ['in'],
        'published': ["exact"],

    }

    search_fields = ['name',"address",'name_bn',"address_bn",'hospital_no','hospital_no_bn','phone_number']
    ordering_fields = ['name','name_bn',"position"]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action=="get_hospital_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin" or user.is_staff:
            return Hospital.objects.filter(profile=False,deleted=False).order_by("position").distinct()
        else:
            # Non-admin user, show only published blog posts
            return Hospital.objects.filter(published=True,profile=False,deleted=False).order_by("position").distinct()
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created hospital {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update hospital {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted hospital {instance.name}",
                timestamp=timezone.now()
            )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['DELETE'], url_path='delete-service/(?P<hospital_id>[^/.]+)/(?P<id>[^/.]+)')
    def delete_service(self, request, id=None, hospital_id = None):
        try:
            service = HospitalService.objects.get(id=id)
            hospital = Hospital.objects.get(id=hospital_id)
            if service in hospital.services.all():
                hospital.services.remove(service)
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted {service.service_name} from {hospital.name} service",
                timestamp=timezone.now()
            )
            return Response({'message': 'Hospital Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except service.DoesNotExist:
            return Response({'message': 'Hospital Service not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'], url_path='get-hospital-by-slug/(?P<slug>[-\w]+)')
    def get_hospital_by_slug(self, request, slug=None):
        try:
            hospital = Hospital.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(hospital)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({'message': 'Hospital not found.'}, status=status.HTTP_404_NOT_FOUND)

class AmbulanceProfileView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsAmbulance]
    serializer_class = AmbulanceProfileManagementSerializer
    queryset = User.objects.filter(role='ambulance')
    
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


class AmbulanceManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = AmbulanceListSerializer
    queryset = Ambulance.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'ac': ['exact'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'published': ["exact"],

        }
    search_fields = ['name','address','name_bn','address_bn','phone_number']
    ordering_fields = ['name','name_bn','position']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action=="get_ambulance_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin" or user.is_staff:
            return Ambulance.objects.filter(profile=False,deleted = False).order_by("position").distinct()
        else:
            # Non-admin user, show only published blog posts
            return Ambulance.objects.filter(published=True,profile=False,deleted = False).order_by("position").distinct()
    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "create" or self.action == "partial_update":
            return AmbulanceManagementSerializer
        return super().get_serializer_class()
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created ambulance {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update ambulance {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted ambulance {instance.name}",
                timestamp=timezone.now()
            )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='get-ambulance-by-slug/(?P<slug>[-\w]+)')
    def get_ambulance_by_slug(self, request, slug=None):
        try:
            ambulance = Ambulance.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(ambulance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({'message': 'Ambulance not found.'}, status=status.HTTP_404_NOT_FOUND)

class AmbulanceFilterApi(viewsets.GenericViewSet):
    serializer_class = AmbulanceListSerializer
    queryset = Ambulance.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'ac': ['exact'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'published': ["exact"],

        }
    search_fields = ['name','address','name_bn','address_bn']
    ordering_fields = ['name','name_bn']

    def list(self, request):
        ac = [False, True]
        if "ac" in request.GET and request.GET.get("ac") == "true":
            ac = [True]
        if "ac" in request.GET and request.GET.get("ac") == "false":
            ac = [False]
        upazila_data = request.GET.get("location__id__in").split(",") if "location__id__in" in request.GET else list(Ambulance.objects.filter(deleted = False,published = True).values_list('location__id', flat=True).distinct())
        district_data = request.GET.get("location__district__id__in").split(",") if "location__district__id__in" in request.GET else list(Ambulance.objects.filter(deleted = False,published = True).values_list('location__district__id', flat=True).distinct())
        division_data = request.GET.get("location__district__division__id__in").split(",") if "location__district__division__id__in" in request.GET else list(Ambulance.objects.filter(deleted = False,published = True).values_list('location__district__division__id', flat=True).distinct())
        filter_district = list(
            Ambulance.objects.filter(
                ac__in = ac,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                published = True,
                deleted = False,
            ).values_list('location__district__id', 'location__district__district_name','location__district__district_name_bn').distinct()
        )
        filter_division = list(
            Ambulance.objects.filter(
                ac__in = ac,
                location__district__id__in = district_data,
                location__id__in = upazila_data,
                published = True,
                deleted = False,
            ).values_list('location__district__division__id', 'location__district__division__division_name','location__district__division__division_name_bn').distinct()
        )

        filter_upazila = list(
            Ambulance.objects.filter(
                ac__in = ac,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                published = True,
                deleted = False,
            ).values_list('location__id', 'location__upazila_name','location__upazila_name_bn').distinct()
        )

        filter_ac = list(
            Ambulance.objects.filter(
                ac=True,
                location__district__id__in=district_data,
                location__id__in = upazila_data,
                published = True,
                deleted = False,
            ).values_list('ac').distinct()
        )
        filter_non_ac = list(
            Ambulance.objects.filter(
                ac=False,
                location__district__id__in=district_data,
                location__id__in = upazila_data,
                published = True,
                deleted = False,
            ).values_list('ac').distinct()
        )

        # Additional filters
        filter_keys = {
            "ac_filters": [
                {
                    "ac": item[0],
                    "count": len(Ambulance.objects.filter(deleted = False,ac=item[0],published = True).distinct())
                } for item in filter_ac
            ],
            "non_ac_filters": [
                {
                    "ac": item[0],
                    "count": len(Ambulance.objects.filter(deleted = False,ac=item[0],published = True).distinct())
                } for item in filter_non_ac
            ]
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name,division_name_bn = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name": division_name,
                "division_name_bn": division_name_bn,
                "count": len(Ambulance.objects.filter(deleted = False,location__district__division__id=division_id,published = True).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name,district_name_bn = district_item
                # Check if the district belongs to the current division
                if Ambulance.objects.filter(deleted = False,location__district__id=district_id, location__district__division__id=division_id,published = True).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "district_name_bn": district_name_bn,
                        "count": len(Ambulance.objects.filter(deleted = False,location__district__id=district_id,published = True).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name,upazila_name_bn = upazila_item
                        # Check if the upazila belongs to the current district
                        if Ambulance.objects.filter(deleted = False,location__id=upazila_id, location__district__id=district_id,published = True).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "upazila_name_bn": upazila_name_bn,
                                "count": len(Ambulance.objects.filter(deleted = False,location__id=upazila_id,published = True).distinct())
                            }
                            

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)

class HospitalFilterApi(viewsets.GenericViewSet):
    queryset = Hospital.objects.filter(profile=False,deleted=False)
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'tests__id': ['in'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'category': ['in'],
        'published': ["exact"],

    }
    search_fields = ['name',"address",'name_bn',"address_bn"]
    ordering_fields = ['name','name_bn']

    def list(self, request):
        specialists_data = request.GET.get("specialists__id__in").split(",") if "specialists__id__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False,published = True).values_list('specialists__id', flat=True).distinct())
        services_data = request.GET.get("services__id__in").split(",") if "services__id__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False,published = True).values_list('services__id', flat=True).distinct())
        upazila_data = request.GET.get("location__id__in").split(",") if "location__id__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False,published = True).values_list('location__id', flat=True).distinct())
        district_data = request.GET.get("location__district__id__in").split(",") if "location__district__id__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False,published = True).values_list('location__district__id', flat=True).distinct())
        division_data = request.GET.get("location__district__division__id__in").split(",") if "location__district__division__id__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False).values_list('location__district__division__id', flat=True).distinct())
        category_data = request.GET.get("category__in").split(",") if "category__in" in request.GET else list(Hospital.objects.filter(deleted=False,profile=False,published = True).values_list('category', flat=True).distinct())
        filter_specialists = list(
            Hospital.objects.filter(
                services__id__in = services_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                category__in = category_data,
                published = True,
                deleted = False,profile = False
            ).values_list('specialists__id', 'specialists__specialist_name','specialists__specialist_name_bn').distinct()
        )
        filter_services = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                category__in = category_data,
                published = True,
                deleted = False,profile = False
            ).values_list('services__id', 'services__service_name','services__service_name_bn').distinct()
        )
        filter_district = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                category__in = category_data,
                published = True,
                deleted = False,profile = False
            ).values_list('location__district__id', 'location__district__district_name','location__district__district_name_bn').distinct()
        )
        filter_division = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__district__id__in = district_data,
                location__id__in = upazila_data,
                category__in = category_data,
                published = True,
                deleted = False,profile = False
            ).values_list('location__district__division__id', 'location__district__division__division_name','location__district__division__division_name_bn').distinct()
        )
        
        filter_upazila = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                category__in = category_data,
                published = True,
                deleted = False,profile = False
            ).values_list('location__id', 'location__upazila_name','location__upazila_name_bn').distinct()
        )
        filter_category = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__district__id__in = district_data,
                location__district__division__id__in = division_data,
                location__id__in = upazila_data,
                published = True,
                deleted = False,profile = False
            ).values_list('category').distinct()
        )

        # Additional filters
        filter_keys = {
            "specialist_filters": [
                {
                    "id": item[0],
                    "specialist_name": item[1],
                    "specialist_name_bn": item[2],
                    "count": len(Hospital.objects.filter(deleted = False,profile = False,specialists__id=item[0],published = True).distinct())
                } for item in filter_specialists
            ],
            "services_filter": [
                {
                    "id": item[0],
                    "services_name": item[1],
                    "services_name_bn": item[2],
                    "count": len(Hospital.objects.filter(deleted = False,profile = False,services__id=item[0],published = True).distinct())
                } for item in filter_services
            ],
            "category_filters": [
                {
                    "category": item[0],
                    "count": len(Hospital.objects.filter(deleted = False,profile = False,category=item[0],published = True).distinct())
                } for item in filter_category
            ],
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name,division_name_bn = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name_bn": division_name_bn,
                "count": len(Hospital.objects.filter(deleted = False,profile = False,location__district__division__id=division_id,published = True).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name,district_name_bn = district_item
                # Check if the district belongs to the current division
                if Hospital.objects.filter(deleted = False,profile = False,location__district__id=district_id, location__district__division__id=division_id,published = True).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "district_name_bn": district_name_bn,
                        "count": len(Hospital.objects.filter(deleted = False,profile = False,location__district__id=district_id,published = True).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name,upazila_name_bn = upazila_item
                        # Check if the upazila belongs to the current district
                        if Hospital.objects.filter(deleted = False,profile = False,location__id=upazila_id, location__district__id=district_id,published = True).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "upazila_name_bn": upazila_name_bn,
                                "count": len(Hospital.objects.filter(deleted = False,profile = False,location__id=upazila_id,published = True).distinct())
                            }
                            

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)

class HospitalProfileListView(viewsets.GenericViewSet):
    permission_classes = [IsHospital,IsAuthenticated]
    serializer_class = HospitalManagementSerializer
    queryset = Hospital.objects.filter(profile=True,deleted = False)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'category': ['in'],
    }
    search_fields = ["user__first_name","user__last_name","user__email","address","hospital_no"]
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
    
class AmbulanceProfileListView(viewsets.GenericViewSet):
    permission_classes = [IsAmbulance,IsHospital,IsAuthenticated]
    serializer_class = AmbulanceManagementSerializer
    queryset = Ambulance.objects.filter(profile=True,deleted = False)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'ac': ['exact'],
        'location__id': ['in'],
        'location__district__id': ['in'],
        'location__district__division__id': ['in'],
        'published': ["exact"],

        }
    search_fields = ["user__first_name","user__last_name","user__email","address","hospital_no"]
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