import datetime
from rest_framework import  status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from appointment.models import DoctorAppointment
from doctor.models import Doctor

from hospital.models import Ambulance, Hospital
from user.models import User
from django.db.models import Q
# model
from .models import ActionLog, Districts, Divisions, Notifications, SiteSettings, Team, Upazilas,Unions,Services,Specialist
# serializer
from .serializers import  ActionLogSerializer, NotificationSerializer, SiteSettingsSerializer, SpecialistSerializer, DivisionSerializer, DistrictSerializer, TeamSerializer, UpazilaSerializer, UnionSerializer,ServicesSerializer
# permissions
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsModerator,IsSuperAdmin
# pagination
from rest_framework.pagination import  LimitOffsetPagination
# filter search sort
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone


class DivisionListAPIView(generics.ListAPIView):
    serializer_class = DivisionSerializer
    queryset = Divisions.objects.all()

class DistrictListAPIView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        division_id = self.kwargs['division_id']
        return Districts.objects.filter(division_id=division_id)

class UpazilaListAPIView(generics.ListAPIView):
    serializer_class = UpazilaSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        return Upazilas.objects.filter(district_id=district_id)
    
class UnionListAPIView(generics.ListAPIView):
    serializer_class = UnionSerializer

    def get_queryset(self):
        upazila = self.kwargs['upazila_id']
        return Unions.objects.filter(upazila=upazila)

class SpecialistManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialistSerializer
    queryset = Specialist.objects.all().distinct()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ['specialist_name','specialist_name_bn']
    ordering_fields = ['specialist_name','specialist_name_bn']

    def get_permissions(self):
        if self.action == "list" or self.action=="get_speicilist_by_slug":
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
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created specialist {instance.specialist_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} updated specialist {instance.specialist_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} deleted specialist {instance.specialist_name}",
                timestamp=timezone.now()
            )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'], url_path='get-specialist-by-slug/(?P<slug>[-\w]+)')
    def get_speicilist_by_slug(self, request, slug=None):
        try:
            blog = Specialist.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Specialist.DoesNotExist:
            return Response({'message': 'Specialist not found.'}, status=status.HTTP_404_NOT_FOUND)

class ServicesManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = ServicesSerializer
    queryset = Services.objects.all().distinct()
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]


    search_fields = ['service_name','service_name_bn']
    ordering_fields = ['service_name','service_name_bn']

    def get_permissions(self):
        if self.action == "list" or self.action=="get_service_by_slug":
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
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} created services {instance.service_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update services {instance.service_name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action=f"{request.user.username} created services {instance.service_name}",
            timestamp=timezone.now()
        )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['GET'], url_path='get-service-by-slug/(?P<slug>[-\w]+)')
    def get_service_by_slug(self, request, slug=None):
        try:
            blog = Services.objects.get(Q(slug=slug)|Q(slug_bn=slug))
            serializer = self.get_serializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Services.DoesNotExist:
            return Response({'message': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class LandingPageReportView(viewsets.GenericViewSet):
    
    def list(self, request, *args, **kwargs):
        data = {}

        data["hospital_count"] = Hospital.objects.filter(profile=False).count()
        data["doctor_count"] = Doctor.objects.filter(profile=False).count()
        data["user_count"] = User.objects.all().count()
        data["donor_count"] = User.objects.filter(profile__donor=True).count()
        data["ambulance_count"] = Ambulance.objects.all().count()

        return Response(data)


class TeamManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = TeamSerializer
    queryset = Team.objects.all().distinct()
    pagination_class = LimitOffsetPagination

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ['name','name_bn',"designation","designation_bn"]
    ordering_fields = ['name','name_bn']

    def get_permissions(self):
        if self.action == "list" :
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
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} add team member info {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action=f"{request.user.username} update team member info {instance.name}",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action=f"{request.user.username} delete team member info {instance.name}",
            timestamp=timezone.now()
        )
        instance.delete()
        return Response({'message':'Successfully deleted.'}, status=status.HTTP_200_OK)
    
class SiteSettingsManagementView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = SiteSettingsSerializer
    queryset = SiteSettings.objects.all()
    pagination_class = LimitOffsetPagination
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many =True)
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object() ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActionLogList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    queryset = ActionLog.objects.all().order_by('-timestamp')
    serializer_class = ActionLogSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class NotificationList(generics.ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetail(generics.RetrieveUpdateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer

    def update(self, request, *args, **kwargs):
        # Extract the list of primary keys from the URL
        pk_list = [int(pk) for pk in kwargs['pk_list'].split(',')]
        
        # Get the instances with the given primary keys
        instances = self.get_queryset().filter(pk__in=pk_list)

        # Check if it's a bulk update request
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(instances, data=data, partial=True, many=True)
        else:
            serializer = self.get_serializer(instances, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    # Add the following method to handle bulk updates
    def perform_update(self, serializer):
        for obj, validated_data in zip(serializer.instance, serializer.validated_data):
            self.update_instance(obj, validated_data)

    def update_instance(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

from django.db.models import Count, Q,Sum
class StatisticsViewSet(viewsets.GenericViewSet):
    def list(self, request):
        # Get today's date
        today = timezone.now()

        # Get start and end of the week
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Get start and end of the month
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(day=1, month=start_of_month.month % 12 + 1) - datetime.timedelta(days=1)

        # Daily Appointments
        daily_appointments = DoctorAppointment.objects.filter(date=today)
        daily_appointments_count = daily_appointments.count()
        daily_fee_total = daily_appointments.aggregate(total_fee=Sum('fee'))['total_fee'] or 0

        # Weekly Appointments
        weekly_appointments = DoctorAppointment.objects.filter(date__range=[start_of_week, end_of_week])
        weekly_appointments_count = weekly_appointments.count()
        weekly_fee_total = weekly_appointments.aggregate(total_fee=Sum('fee'))['total_fee'] or 0

        # Monthly Appointments
        monthly_appointments = DoctorAppointment.objects.filter(date__range=[start_of_month, end_of_month])
        monthly_appointments_count = monthly_appointments.count()
        monthly_fee_total = monthly_appointments.aggregate(total_fee=Sum('fee'))['total_fee'] or 0

        # Overall Appointments
        total_appointments = DoctorAppointment.objects.all()
        total_appointments_count = total_appointments.count()
        total_fee_total = total_appointments.aggregate(total_fee=Sum('fee'))['total_fee'] or 0

        # Doctor with most appointments
        most_appointment_doctor = DoctorAppointment.objects.values('doctor__name').annotate(num_appointments=Count('doctor')).order_by('-num_appointments').first()

        # Ratio of new to old patients
        new_patients = DoctorAppointment.objects.filter(patientstatus='new').count()
        old_patients = DoctorAppointment.objects.filter(patientstatus='old').count()
        ratio_new_old_patients = new_patients / old_patients if old_patients != 0 else 0

        # Number of canceled appointments
        canceled_appointments = DoctorAppointment.objects.filter(status='canceled').count()

        # Number of done appointments
        done_appointments = DoctorAppointment.objects.filter(status='done').count()

        # Return statistics as response
        statistics_data = {
            "daily_appointments_count": daily_appointments_count,
            "daily_fee_total": daily_fee_total,
            "weekly_appointments_count": weekly_appointments_count,
            "weekly_fee_total": weekly_fee_total,
            "monthly_appointments_count": monthly_appointments_count,
            "monthly_fee_total": monthly_fee_total,
            "total_appointments_count": total_appointments_count,
            "total_fee_total": total_fee_total,
            "most_appointment_doctor": most_appointment_doctor,
            "ratio_new_old_patients": ratio_new_old_patients,
            "canceled_appointments": canceled_appointments,
            "done_appointments": done_appointments
        }

        return Response(statistics_data)
