from django.shortcuts import get_object_or_404
from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
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
            return Response({'message': 'Experience not found.'}, status=status.HTTP_404_NOT_FOUND)    @action(detail=False, methods=['DELETE'], url_path='cancel-appointment/(?P<id>[^/.]+)')
           


class DoctorManagementView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorManagementSerializer
    queryset = Doctor.objects.filter(profile=False)
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
    search_fields = ['name',"address",'name_bn',"address_bn",'license_no','license_no_bn']
    ordering_fields = ['name','name_bn']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or  self.action=="get_doctor_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by("-id")
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
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
        self.get_object().delete()
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
            chamber.delete()  # Delete the chamber
            return Response({'message': 'Chamber deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Chamber.DoesNotExist:
            return Response({'message': 'Chamber not found.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['DELETE'], url_path='delete-experience/(?P<id>[^/.]+)')
    def delete_experience(self, request, id=None):
        try:
            experience = Experience.objects.get(id=id)
            experience.delete()  # Delete the chamber
            return Response({'message': 'Experience deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Experience.DoesNotExist:
            return Response({'message': 'Experience not found.'}, status=status.HTTP_404_NOT_FOUND)    @action(detail=False, methods=['DELETE'], url_path='cancel-appointment/(?P<id>[^/.]+)')
            
class DoctorFilterApi(viewsets.GenericViewSet):
    queryset = Doctor.objects.filter(profile=False)
    filter_backends = [SearchFilter, DjangoFilterBackend]

    filterset_fields = {
        'specialists__id': ['in'],
        'services__id': ['in'],
        'location__union_name': ['in'],
        'location__upazila__id': ['in'],
        'location__upazila__district__id': ['in'],
        'location__upazila__district__division__id': ['in'],
    }

    search_fields = ['name',"address",'name_bn',"address_bn",'chamber__hospital__name']
    ordering_fields = ['name','name_bn']

    def list(self, request):
        specialists_data = request.GET.get("specialists__id__in").split(",") if "specialists__id__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('specialists__id', flat=True).distinct())
        doctorservices_data = request.GET.get("services__id__in").split(",") if "services__id__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('services__id', flat=True).distinct())
        union_data = request.GET.get("location__union_name__in").split(",") if "location__union_name__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('location__union_name', flat=True).distinct())
        upazila_data = request.GET.get("location__upazila__id__in").split(",") if "location__upazila__id__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('location__upazila__id', flat=True).distinct())
        district_data = request.GET.get("location__upazila__district__id__in").split(",") if "location__upazila__district__id__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('location__upazila__district__id', flat=True).distinct())
        division_data = request.GET.get("location__upazila__district__division__id__in").split(",") if "location__upazila__district__division__id__in" in request.GET else list(Doctor.objects.filter(profile=False).values_list('location__upazila__district__division__id', flat=True).distinct())
        filter_specialists = list(
            Doctor.objects.filter(
                services__id__in = doctorservices_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('specialists__id', 'specialists__specialist_name','specialists__specialist_name_bn').distinct()
        )
        filter_doctorservices = list(
            Doctor.objects.filter(
                specialists__id__in = specialists_data,
                location__upazila__district__id__in = district_data,
                location__upazila__district__division__id__in = division_data,
                location__upazila__id__in = upazila_data,
                location__union_name__in = union_data,
            ).values_list('services__id', 'services__service_name','services__service_name_bn').distinct()
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
            ).values_list('location__union_name').distinct()
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
                    "specialist_name_bn": item[2],
                    "count": len(Doctor.objects.filter(specialists__id=item[0]).distinct())
                } for item in filter_specialists
            ],
            "doctorservices_filter": [
                {
                    "id": item[0],
                    "services_name": item[1],
                    "services_name_bn": item[1],
                    "count": len(Doctor.objects.filter(services__id=item[0]).distinct())
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
                "count": len(Doctor.objects.filter(location__upazila__district__division__id=division_id).distinct())
            }
            # Initialize an empty list to hold district filters
            division_data["district_filter"] = []
            
            # Iterate over district filters
            for district_item in filter_district:
                district_id, district_name = district_item
                # Check if the district belongs to the current division
                if Doctor.objects.filter(location__upazila__district__id=district_id, location__upazila__district__division__id=division_id).exists():
                    # Initialize district data
                    district_data = {
                        "id": district_id,
                        "district_name": district_name,
                        "count": len(Doctor.objects.filter(location__upazila__district__id=district_id).distinct())
                    }
                    # Initialize an empty list to hold upazila filters
                    district_data["upazila_filter"] = []

                    # Iterate over upazila filters
                    for upazila_item in filter_upazila:
                        upazila_id, upazila_name = upazila_item
                        # Check if the upazila belongs to the current district
                        if Doctor.objects.filter(location__upazila__id=upazila_id, location__upazila__district__id=district_id).exists():
                            # Initialize upazila data
                            upazila_data = {
                                "id": upazila_id,
                                "upazila_name": upazila_name,
                                "count": len(Doctor.objects.filter(location__upazila__id=upazila_id).distinct())
                            }
                            # Initialize an empty list to hold union filters
                            upazila_data["union_filter"] = []

                            # Iterate over union filters
                            for union_item in filter_union:
                                union_name = union_item[0]
                                # Check if the union belongs to the current upazila
                                if Doctor.objects.filter(location__union_name=union_name, location__upazila__id=upazila_id).exists():
                                    # Add union data
                                    union_data = {
                                        "union_name": union_name,
                                        "count": len(Doctor.objects.filter(location__union_name=union_name).distinct())
                                    }
                                    upazila_data["union_filter"].append(union_data)

                            district_data["upazila_filter"].append(upazila_data)

                    division_data["district_filter"].append(district_data)

            filter_keys.setdefault("division_filters", []).append(division_data)

        response_data = filter_keys

        return Response(response_data, status=status.HTTP_200_OK)
    

class DoctorProfileListView(viewsets.GenericViewSet):
    permission_classes = [IsDoctor,IsAuthenticated]
    serializer_class = DoctorManagementSerializer
    queryset = Doctor.objects.filter(profile=True)
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
    permission_classes = [IsAuthenticated]
    queryset =Review.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['user__first_name']

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = []
        if self.action == "delete":
            self.permission_classes = [IsAuthenticated, IsModerator]
        return super().get_permissions()

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
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


    @action(detail=False, methods=['PATCH'])
    def update_reviews(self, request):
        if request.method == 'PATCH':
            for data in request.data:
                new_rating = data.get("rating")
                new_content = data.get("content")
                order_id = data.get("order")
                product_id = data.get("product")
                try:
                    review = get_object_or_404(Review, order=order_id, product=product_id)
                    review.rating = new_rating
                    review.content = new_content
                    review.save()
                except Review.DoesNotExist:
                    pass

            return Response({"message": "Reviews updated successfully"})

        return Response(status=400, data={"message": "Invalid request method"})
    

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response({'status':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
