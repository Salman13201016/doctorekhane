from django.shortcuts import render
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# filter search sort
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hospital
from .serializers import HospitalManagementSerializer,AmbulanceListSerializer
# pagination
from rest_framework.pagination import  LimitOffsetPagination
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin,IsHospital
# Create your views here.
class HospitalManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsHospital]
    serializer_class = HospitalManagementSerializer
    queryset = Hospital.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
        'category': ['in'],
    }
    search_fields = ['name',"address"]
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action=="get_hospital_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
    def list(self, request):
        # Apply filters
        queryset = self.filter_queryset(self.get_queryset()).order_by('-id')

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,requst):
        serializer =self.get_serializer(data=requst.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'], url_path='get-hospital-by-slug/(?P<slug>[-\w]+)')
    def get_hospital_by_slug(self, request, slug=None):
        try:
            hospital = Hospital.objects.get(slug=slug)
            serializer = self.get_serializer(hospital)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({'message': 'Hospital not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class AmbulanceListView(viewsets.GenericViewSet):
    serializer_class = AmbulanceListSerializer
    queryset = Hospital.objects.all().exclude(ambulance = False)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    # filterset_fields = ['is_superuser','is_staff',]
    filterset_fields = {
        'ac': ['exact'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
        }
    search_fields = ['name','address']

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AmbulanceFilterApi(viewsets.GenericViewSet):
    serializer_class = AmbulanceListSerializer
    queryset = Hospital.objects.all().exclude(ambulance = False)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        'ac': ['exact'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
        }
    search_fields = ['name','address']
    ordering_fields = ['name']

    def list(self, request):
        ac = [False, True]
        if "ac" in request.GET and request.GET.get("ac") == "true":
            ac = [True]
        if "ac" in request.GET and request.GET.get("ac") == "false":
            ac = [False]
        union_data = request.GET.get("location__union_name__in").split(",") if "location__union_name__in" in request.GET else list(Hospital.objects.all().exclude(ambulance = False).values_list('location__union_name', flat=True).distinct())
        upazila_data = request.GET.get("location__upazila__id__in").split(",") if "location__upazila__id__in" in request.GET else list(Hospital.objects.all().exclude(ambulance = False).values_list('location__upazila__id', flat=True).distinct())
        district_data = request.GET.get("location__upazila__district__id__in").split(",") if "location__upazila__district__id__in" in request.GET else list(Hospital.objects.all().exclude(ambulance = False).values_list('location__upazila__district__id', flat=True).distinct())
        division_data = request.GET.get("location__upazila__district__division__id__in").split(",") if "location__upazila__district__division__id__in" in request.GET else list(Hospital.objects.all().exclude(ambulance = False).values_list('location__upazila__district__division__id', flat=True).distinct())
        filter_district = list(
            Hospital.objects.filter(
                ac__in = ac,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('location__upazila__district__id', 'location__upazila__district__district_name').distinct()
        )
        filter_division = list(
            Hospital.objects.filter(
                ac__in = ac,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('location__upazila__district__division__id', 'location__upazila__district__division__division_name').distinct()
        )
        filter_union = list(
            Hospital.objects.filter(
                ac__in = ac,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__upazila__district__division__id__in = division_data,
            ).values_list('location__union_name', 'location__union_name').distinct()
        )
        filter_upazila = list(
            Hospital.objects.filter(
                ac__in = ac,
                location__upazila__district__id__in = district_data,
                location__union_name__in = union_data,
                location__upazila__district__division__id__in = division_data,
            ).values_list('location__upazila__id', 'location__upazila__upazila_name').distinct()
        )

        filter_ac = list(
            Hospital.objects.filter(
                ac=True,
                location__upazila__district__id__in=district_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('ac').distinct()
        )
        filter_non_ac = list(
            Hospital.objects.filter(
                ac=False,
                location__upazila__district__id__in=district_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('ac').distinct()
        )

        # Additional filters
        filter_keys = {
            "ac_filters": [
                {
                    "ac": item[0],
                    "count": len(Hospital.objects.filter(ac=item[0],ambulance = True).distinct())
                } for item in filter_ac
            ],
            "non_ac_filters": [
                {
                    "ac": item[0],
                    "count": len(Hospital.objects.filter(ac=item[0],ambulance = True).distinct())
                } for item in filter_non_ac
            ]
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name": division_name,
                "count": len(Hospital.objects.filter(location__upazila__district__division__id=division_id,ambulance = True).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name = district_item
                # Check if the district belongs to the current division
                if Hospital.objects.filter(location__upazila__district__id=district_id, location__upazila__district__division__id=division_id,ambulance = True).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "count": len(Hospital.objects.filter(location__upazila__district__id=district_id,ambulance = True).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name = upazila_item
                        # Check if the upazila belongs to the current district
                        if Hospital.objects.filter(location__upazila__id=upazila_id, location__upazila__district__id=district_id,ambulance = True).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "count": len(Hospital.objects.filter(location__upazila__id=upazila_id,ambulance = True).distinct())
                            }
                            # Initialize an empty list to hold union filters
                            upazila_data["union_filter"] = []

                            # Iterate over union filters
                            for union_item in filter_union:
                                union_name = union_item[0]
                                # Check if the union belongs to the current upazila
                                if Hospital.objects.filter(location__union_name=union_name, location__upazila__id=upazila_id,ambulance = True).exists():
                                    # Add union data
                                    union_data = {
                                        "union_name": union_name,
                                        "count": len(Hospital.objects.filter(location__union_name=union_name,ambulance = True).distinct())
                                    }
                                    upazila_data["union_filter"].append(union_data)

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)

class HospitalFilterApi(viewsets.GenericViewSet):
    queryset = Hospital.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
        'category': ['in'],
    }
    search_fields = ['name',"address"]
    ordering_fields = ['name']

    def list(self, request):
        specialists_data = request.GET.get("specialists__id__in").split(",") if "specialists__id__in" in request.GET else list(Hospital.objects.all().values_list('specialists__id', flat=True).distinct())
        services_data = request.GET.get("services__id__in").split(",") if "services__id__in" in request.GET else list(Hospital.objects.all().values_list('services__id', flat=True).distinct())
        union_data = request.GET.get("location__union_name__in").split(",") if "location__union_name__in" in request.GET else list(Hospital.objects.all().values_list('location__union_name', flat=True).distinct())
        upazila_data = request.GET.get("location__upazila__id__in").split(",") if "location__upazila__id__in" in request.GET else list(Hospital.objects.all().values_list('location__upazila__id', flat=True).distinct())
        district_data = request.GET.get("location__upazila__district__id__in").split(",") if "location__upazila__district__id__in" in request.GET else list(Hospital.objects.all().values_list('location__upazila__district__id', flat=True).distinct())
        division_data = request.GET.get("location__upazila__district__division__id__in").split(",") if "location__upazila__district__division__id__in" in request.GET else list(Hospital.objects.all().values_list('location__upazila__district__division__id', flat=True).distinct())
        category_data = request.GET.get("category__in").split(",") if "category__in" in request.GET else list(Hospital.objects.all().values_list('category', flat=True).distinct())
        filter_specialists = list(
            Hospital.objects.filter(
                services__id__in = services_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
                category__in = category_data
            ).values_list('specialists__id', 'specialists__specialist_name').distinct()
        )
        filter_services = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
                category__in = category_data
            ).values_list('services__id', 'services__service_name').distinct()
        )
        filter_district = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
                category__in = category_data
            ).values_list('location__upazila__district__id', 'location__upazila__district__district_name').distinct()
        )
        filter_division = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
                category__in = category_data
            ).values_list('location__upazila__district__division__id', 'location__upazila__district__division__division_name').distinct()
        )
        filter_union = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__upazila__district__id__in = district_data,
                location__upazila__id__in = upazila_data,
                location__upazila__district__division__id__in = division_data,
                category__in = category_data
            ).values_list('location__union_name').distinct()
        )
        filter_upazila = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__upazila__district__id__in = district_data,
                location__union_name__in = union_data,
                location__upazila__district__division__id__in = division_data,
                category__in = category_data
            ).values_list('location__upazila__id', 'location__upazila__upazila_name').distinct()
        )
        filter_category = list(
            Hospital.objects.filter(
                specialists__id__in = specialists_data,
                services__id__in = services_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('category').distinct()
        )

        # Additional filters
        filter_keys = {
            "specialist_filters": [
                {
                    "id": item[0],
                    "specialist_name": item[1],
                    "count": len(Hospital.objects.filter(specialists__id=item[0]).distinct())
                } for item in filter_specialists
            ],
            "division_filters": [
                {
                    "id": item[0],
                    "division_name": item[1],
                    "count": len(Hospital.objects.filter(location__upazila__district__division__id=item[0]).distinct())
                } for item in filter_division
            ],
            "services_filter": [
                {
                    "id": item[0],
                    "services_name": item[1],
                    "count": len(Hospital.objects.filter(services__id=item[0]).distinct())
                } for item in filter_services
            ],
            "category_filters": [
                {
                    "category": item[0],
                    "count": len(Hospital.objects.filter(category=item[0]).distinct())
                } for item in filter_category
            ],
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name": division_name,
                "count": len(Hospital.objects.filter(location__upazila__district__division__id=division_id).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name = district_item
                # Check if the district belongs to the current division
                if Hospital.objects.filter(location__upazila__district__id=district_id, location__upazila__district__division__id=division_id).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "count": len(Hospital.objects.filter(location__upazila__district__id=district_id).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name = upazila_item
                        # Check if the upazila belongs to the current district
                        if Hospital.objects.filter(location__upazila__id=upazila_id, location__upazila__district__id=district_id).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "count": len(Hospital.objects.filter(location__upazila__id=upazila_id).distinct())
                            }
                            # Initialize an empty list to hold union filters
                            upazila_data["union_filter"] = []

                            # Iterate over union filters
                            for union_item in filter_union:
                                union_name = union_item[0]
                                # Check if the union belongs to the current upazila
                                if Hospital.objects.filter(location__union_name=union_name, location__upazila__id=upazila_id).exists():
                                    # Add union data
                                    union_data = {
                                        "union_name": union_name,
                                        "union_count": len(Hospital.objects.filter(location__union_name=union_name).distinct())
                                    }
                                    upazila_data["union_filter"].append(union_data)

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)
