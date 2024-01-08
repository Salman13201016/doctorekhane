from django.shortcuts import render
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# filter search sort
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hospital
from .serializers import HospitalManagementSerializer, HospitalProfileSerializer
# pagination
from rest_framework.pagination import  LimitOffsetPagination
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsAdmin
# Create your views here.
class HospitalManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = HospitalManagementSerializer
    queryset = Hospital.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]

    filterset_fields = {
        'services_offered': ["in"],
        'specialties': ["in"],
        'name': ["exact"],
        'division': ["exact"],
        'district': ["exact"],
        'state': ["exact"],
    }
    search_fields = ['name','specialties','services_offered']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action=="get_blog_by_slug":
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
        return Response({'status':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'], url_path='get-hospital-by-slug/(?P<slug>[-\w]+)')
    def get_blog_by_slug(self, request, slug=None):
        try:
            hospital = Hospital.objects.get(slug=slug)
            serializer = self.get_serializer(hospital)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({'detail': 'Hospital not found.'}, status=status.HTTP_404_NOT_FOUND)

class HospitalProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalProfileSerializer

