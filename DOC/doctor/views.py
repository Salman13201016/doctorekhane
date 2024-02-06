from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

# model
from .models import Specialist
# serializer
from rest_framework import serializers
from .serializers import  SpecialistSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator 

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