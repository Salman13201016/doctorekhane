from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

# model
from .models import AppointmentInfo, DoctorAppointment, TestAppointment
from user.models import User
# serializer
from rest_framework import serializers
from .serializers import  AppointmentInfoSerializer, DoctorAppointmentManagementSerializer, TestAppointmentManagementSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsSuperAdmin, IsModerator,IsDoctor

# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from DOC.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
# Create your views here.
class DoctorAppointmentManagementView(viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = DoctorAppointmentManagementSerializer
    queryset = DoctorAppointment.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'patientstatus': ['exact'],
        'date': ['range'],
        'time': ['range'],
        'status': ['exact'],
    }
    search_fields = ['appointment_id',"user__first_name","user__last_name","doctor__name"]
    ordering_fields = ['id']

    
    def retrieve(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            # Assuming the user's ID is linked to the instance (for example, in user field)
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():  # Check if queryset is empty
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            appointment = serializer.save()
            # Send email to the user
            subject = 'Appointment Confirmation'
            message = f'Your appointment with {appointment.doctor} on {appointment.date} at {appointment.time} has been successfully booked.'
            from_email = DEFAULT_FROM_EMAIL
            to_email = appointment.user.email

            send_mail(subject, message, from_email, [to_email])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.role == 'doctor':
            queryset = DoctorAppointment.objects.filter(doctor__email=request.user.email)
        elif request.user.role == 'general':
            queryset = DoctorAppointment.objects.filter(user=request.user)
        else:
            queryset = DoctorAppointment.objects.all()
        
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = self.get_object()

        # Check if the user is admin or superuser
        if request.user.role == "admin" or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": "You are not authorized to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists(): 
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['PATCH'], url_path='cancel-appointment/(?P<id>[^/.]+)')
    def cancel_appointment(self, request, id, slug=None):
        try:
            appointment = self.get_queryset().get(id=id)
        except DoctorAppointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the appointment belongs to the logged-in user
        if appointment.user != request.user:
            return Response({'error': 'You are not authorized to cancel this appointment'}, status=status.HTTP_403_FORBIDDEN)

        appointment.status = 'cancel'
        # Send email to the user
        subject = 'Appointment Cancelation'
        message = f'Your appointment with {appointment.doctor} on {appointment.date} at {appointment.time} has been successfully canceled.'
        from_email = DEFAULT_FROM_EMAIL
        to_email = appointment.user.email

        send_mail(subject, message, from_email, [to_email])
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class TestAppointmentManagementView(viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = TestAppointmentManagementSerializer
    queryset = TestAppointment.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend,OrderingFilter]

    filterset_fields = {
        'private': ['exact'],
        'date': ['range'],
        'time': ['range'],
        'status': ['exact'],
    }
    search_fields = ['appointment_id',"user__first_name","user__last_name","test__test_name"]
    ordering_fields = ['id']

    
    def retrieve(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            # Assuming the user's ID is linked to the instance (for example, in user field)
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():  # Check if queryset is empty
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            appointment = serializer.save()
            # Send email to the user
            subject = 'Test Appointment Confirmation'
            message = f'Your test appointment for {appointment.test} at {appointment.hospital} on {appointment.date} at {appointment.time} has been successfully booked.'
            from_email = DEFAULT_FROM_EMAIL
            to_email = appointment.user.email

            send_mail(subject, message, from_email, [to_email])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.role == 'hospital':
            queryset = TestAppointment.objects.filter(hospital__user=request.user)
        elif request.user.role == 'general':
            queryset = TestAppointment.objects.filter(user=request.user)
        else:
            queryset = TestAppointment.objects.all()
        
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists():
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            instance = self.get_object()
        else:
            queryset = self.get_queryset().filter(user=request.user)
            if not queryset.exists(): 
                return Response({"message": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
            instance = get_object_or_404(queryset)
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)    
    
    @action(detail=False, methods=['PATCH'], url_path='cancel-appointment/(?P<id>[^/.]+)')
    def cancel_test_appointment(self, request, id, slug=None):
        try:
            test_appointment = self.get_queryset().get(id=id)
        except TestAppointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the appointment belongs to the logged-in user
        if test_appointment.user != request.user:
            return Response({'error': 'You are not authorized to cancel this appointment'}, status=status.HTTP_403_FORBIDDEN)

        test_appointment.status = 'cancel'
        # Send email to the user
        subject = 'Test Appointment Canceled'
        message = f'Your test appointment for {test_appointment.test} at {test_appointment.hospital} on {test_appointment.date} at {test_appointment.time} has been successfully canceled.'
        from_email = DEFAULT_FROM_EMAIL
        to_email = test_appointment.user.email

        send_mail(subject, message, from_email, [to_email])
        test_appointment.save()
        serializer = self.get_serializer(test_appointment)
        return Response(serializer.data)



class AppointmentInfoManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsSuperAdmin]
    serializer_class = AppointmentInfoSerializer
    queryset = AppointmentInfo.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'patient_gender': ['exact'],
        'date': ['range'],
        'time': ['range'],
        'patient_type': ['exact'],
        'ref_doctor__id': ['in'],

    }
    search_fields = ['invoice_id','patient_id','patient_name','patient_id','invoice_id','patient_id',"contact_no","ref_doctor__name"]
    ordering_fields = ['id']
    
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
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)