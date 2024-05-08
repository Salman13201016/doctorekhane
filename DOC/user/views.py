from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# model
# from django.contrib.auth.models import User
from user.models import User
# serializer
from rest_framework import serializers
from .serializers import  DonorListSerializer, SuperUserManagementSerializer, UserManagementSerializer, UserProfileSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator 

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

'''
    This serializer is used for logged in user
'''
class ProfileView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.filter(role='general')

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


'''
👉 This view is used for admin
👉 who can management locations
'''

class UserManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = UserManagementSerializer
    queryset = User.objects.filter(role="general").exclude(is_superuser=True).distinct()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    # filterset_fields = ['is_superuser','is_staff',]
    filterset_fields = ['role']
    search_fields = ['first_name', 'last_name', 'email','profile__phone_number']

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
        if requested_user.role=="admin":
            raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
        requested_user.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)


class SuperUserManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = SuperUserManagementSerializer
    queryset = User.objects.filter(role="general").exclude(is_superuser=True)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = ['role']
    search_fields = ['first_name', 'last_name', 'email','profile__phone_number']

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
        self.get_object().delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)

    
class DonorListView(viewsets.GenericViewSet):
    serializer_class = DonorListSerializer
    queryset = User.objects.filter(role="general").exclude(profile__donor = False).distinct()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'profile__blood_group': ['in'],
        'profile__location__union_name': ['in'],
        'profile__location__upazila__id': ['in'],
        'profile__location__upazila__district__id': ['in'],
        'profile__location__upazila__district__division__id': ['in'],
        }
    search_fields = ['profile__blood_group','profile__address']

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DonorFilterApi(viewsets.GenericViewSet):
    queryset = User.objects.filter(role="general").exclude(profile__donor = False)
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'profile__blood_group': ['in'],
        'profile__location__union_name': ['in'],
        'profile__location__upazila__id': ['in'],
        'profile__location__upazila__district__id': ['in'],
        'profile__location__upazila__district__division__id': ['in'],
        }
    search_fields = ['profile__blood_group','profile__address']

    def list(self, request):
        blood_group_data = request.GET.get("profile__blood_group__in").split(",") if "profile__blood_group__in" in request.GET else list(User.objects.filter(role="general").exclude(profile__donor = False).values_list('profile__blood_group', flat=True).distinct())
        union_data = request.GET.get("profile__location__union_name__in").split(",") if "profile__location__union_name__in" in request.GET else list(User.objects.filter(role="general").exclude(profile__donor = False).values_list('profile__location__union_name', flat=True).distinct())
        upazila_data = request.GET.get("profile__location__upazila__id__in").split(",") if "profile__location__upazila__id__in" in request.GET else list(User.objects.filter(role="general").exclude(profile__donor = False).values_list('profile__location__upazila__id', flat=True).distinct())
        district_data = request.GET.get("profile__location__upazila__district__id__in").split(",") if "profile__location__upazila__district__id__in" in request.GET else list(User.objects.filter(role="general").exclude(profile__donor = False).values_list('profile__location__upazila__district__id', flat=True).distinct())
        division_data = request.GET.get("profile__location__upazila__district__division__id__in").split(",") if "profile__location__upazila__district__division__id__in" in request.GET else list(User.objects.filter(role="general").exclude(profile__donor = False).values_list('profile__location__upazila__district__division__id', flat=True).distinct())
        filter_blood_group = list(
            User.objects.filter(
                profile__location__upazila__district__id__in = district_data,
                profile__location__upazila__district__division__id__in = division_data,
                profile__location__upazila__id__in = upazila_data,
                profile__location__union_name__in = union_data,
            ).values_list('profile__blood_group').distinct()
        )
        filter_district = list(
            User.objects.filter(
                profile__blood_group__in = blood_group_data,
                profile__location__upazila__district__division__id__in = division_data,
                profile__location__upazila__id__in = upazila_data,
                profile__location__union_name__in = union_data,
            ).values_list('profile__location__upazila__district__id', 'profile__location__upazila__district__district_name').distinct()
        )
        filter_division = list(
            User.objects.filter(
                profile__blood_group__in = blood_group_data,
                profile__location__upazila__district__id__in = district_data,
                profile__location__upazila__id__in = upazila_data,
                profile__location__union_name__in = union_data,
            ).values_list('profile__location__upazila__district__division__id', 'profile__location__upazila__district__division__division_name').distinct()
        )
        filter_union = list(
            User.objects.filter(
                profile__blood_group__in = blood_group_data,
                profile__location__upazila__district__id__in = district_data,
                profile__location__upazila__id__in = upazila_data,
                profile__location__upazila__district__division__id__in = division_data,
            ).values_list('profile__location__union_name', 'profile__location__union_name').distinct()
        )
        filter_upazila = list(
            User.objects.filter(
                profile__blood_group__in = blood_group_data,
                profile__location__upazila__district__id__in = district_data,
                profile__location__union_name__in = union_data,
                profile__location__upazila__district__division__id__in = division_data,
            ).values_list('profile__location__upazila__id', 'profile__location__upazila__upazila_name').distinct()
        )

        # Additional filters
        filter_keys = {
            "blood_group_filter": [
                {
                    "blood_group": item[0],
                    "count": len(User.objects.filter(profile__blood_group=item[0],profile__donor=True).distinct())
                } for item in filter_blood_group
            ]
        }
        # Iterate over division filters
        for division_item in filter_division:
            division_id, division_name = division_item
            # Initialize division data
            division_data = {
                "id": division_id,
                "division_name": division_name,
                "count": len(User.objects.filter(profile__location__upazila__district__division__id=division_id,profile__donor=True).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name = district_item
                # Check if the district belongs to the current division
                if User.objects.filter(profile__location__upazila__district__id=district_id, profile__location__upazila__district__division__id=division_id,profile__donor=True).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "count": len(User.objects.filter(profile__location__upazila__district__id=district_id,profile__donor=True).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name = upazila_item
                        # Check if the upazila belongs to the current district
                        if User.objects.filter(profile__location__upazila__id=upazila_id, profile__location__upazila__district__id=district_id,profile__donor=True).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "count": len(User.objects.filter(profile__location__upazila__id=upazila_id,profile__donor=True).distinct())
                            }
                            # Initialize an empty list to hold union filters
                            upazila_data["union_filter"] = []

                            # Iterate over union filters
                            for union_item in filter_union:
                                union_name = union_item[0]
                                # Check if the union belongs to the current upazila
                                if User.objects.filter(profile__location__union_name=union_name, profile__location__upazila__id=upazila_id,profile__donor=True).exists():
                                    # Add union data
                                    union_data = {
                                        "union_name": union_name,
                                        "count": len(User.objects.filter(profile__location__union_name=union_name,profile__donor=True).distinct())
                                    }
                                    upazila_data["union_filter"].append(union_data)

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)