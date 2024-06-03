import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from DOC.settings import DEFAULT_FROM_EMAIL
from django.views.decorators.csrf import csrf_exempt

from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.pagination import  LimitOffsetPagination

@csrf_exempt
def contact_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            # Extract data from request
            name = data.get('name', '')
            email = data.get('email', '')
            phone = data.get('phone', '')
            message = data.get('message', '')
            
            # Save data to the database
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            subject = 'Inquiry from ' + name
            message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'
            from_email = DEFAULT_FROM_EMAIL
            to_email = DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, [to_email], fail_silently=True)

            return JsonResponse({"message": "Form submitted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

class ContactMessageViewSet(viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter,DjangoFilterBackend]
    filterset_fields = {
        'created_at': ['range'],
    }
    search_fields = ['name', 'email', 'phone',]
    ordering_fields = ['created_at']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
