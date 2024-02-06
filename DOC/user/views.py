from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# model
from django.contrib.auth.models import User
# serializer
from rest_framework import serializers
from .serializers import  SuperUserManagementSerializer, UserManagementSerializer, UserProfileSerializer
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
    queryset = User.objects.all()

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
    queryset = User.objects.all().exclude(is_superuser=True)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    # filterset_fields = ['is_superuser','is_staff',]
    filterset_fields = ['profile__role']
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
        if requested_user.profile.role=="admin":
            raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
        requested_user.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

class SuperUserManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = SuperUserManagementSerializer
    queryset = User.objects.all().exclude(is_superuser=True)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['profile__role']
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
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    