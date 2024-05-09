from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
import requests
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# filter search sort
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.models import ActionLog
from .models import Blog
from .serializers import BlogManagementSerializer
# pagination
from rest_framework.pagination import  LimitOffsetPagination
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsDoctor, IsModerator

# Create your views here.
class BlogManagementView(viewsets.GenericViewSet):
    permission_classes = [IsSuperAdmin,IsModerator]
    serializer_class = BlogManagementSerializer
    queryset = Blog.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'title': ["in"],
        'time': ["range"],
        'published': ["exact"],
    }
    search_fields = ['title']
    ordering_fields = ['time']
    
    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or  self.action=="get_blog_by_slug":
            self.permission_classes = []
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin" or user.is_staff:
            # Admin user, show all blog posts
            return Blog.objects.all().order_by('-id')
        else:
            # Non-admin user, show only published blog posts
            return Blog.objects.filter(published=True).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.request.user,
                action=f"{request.user.username} write a blog {instance.title}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        old_publish_status = instance.publish

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()

            # Check if 'publish' field has been updated
            if instance.publish != old_publish_status:
                # Log action for change in publish status
                ActionLog.objects.create(
                    user=request.user,
                    action=f"{request.user.username} {'published' if instance.published else 'unpublished'} a blog '{instance.title}'",
                    timestamp=timezone.now()
                )

            # Log action for other field changes
            other_changes = [key for key, value in serializer.validated_data.items() if key != 'published']
            if other_changes:
                action_description = ', '.join(other_changes)
                ActionLog.objects.create(
                    user=request.user,
                    action=f"{request.user.username} updated a blog {action_description}",
                    timestamp=timezone.now()
                )

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted a blog {instance.name}",
                timestamp=timezone.now()
            )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['GET'], url_path='get-blog-by-slug/(?P<slug>[-\w]+)')
    def get_blog_by_slug(self, request, slug=None):
        try:
            blog = Blog.objects.get(slug=slug)
            serializer = self.get_serializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class PersonalBlogManagementView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsDoctor]
    serializer_class = BlogManagementSerializer
    queryset = Blog.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]


    filterset_fields = {
        'title': ["in"],
        'time': ["exact"],
    }
    search_fields = ['title', 'time']
    ordering_fields = ['time']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(author=request.user)

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return Response({'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return Response({'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response({'message': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='get-blog-by-slug/(?P<slug>[-\w]+)')
    def get_blog_by_slug(self, request, slug=None):
        try:
            blog = Blog.objects.get(slug=slug)
            serializer = self.get_serializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
      