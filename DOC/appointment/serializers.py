from rest_framework import serializers

from doctor.serializers import ChamberSerializer
from .models import DoctorAppointment,TestAppointment

class DoctorAppointmentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorAppointment
        fields = "__all__"
        extra_kwargs = {
            'appointment_id': {'read_only': True},
            'fee': {'required': False},
            'comment': {'required': False},
        }
    def create(self, validated_data):
        doctor_id = validated_data['doctor'].id
        user_id = validated_data['user'].id
        chamber_id = validated_data['chamber'].id
        date = validated_data['date'].strftime('%Y%m%d')
        time = validated_data['time'].strftime('%H%M')
        
        # Generate appointment_id based on specified format
        validated_data['appointment_id'] = f"{doctor_id}{chamber_id}{date}{time}{user_id}"
        
        # Set fee from chamber.fee
        if validated_data['patientstatus'] == 'new':
            validated_data['fee'] = int(validated_data['chamber'].fee.split('|')[1])
        else:
            validated_data['fee'] = int(validated_data['chamber'].fee.split('|')[0])
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.user:
            representation['user_id'] = instance.user.id
            representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"

        if instance.doctor:
            representation['doctor_id'] = instance.doctor.id
            representation['doctor'] = instance.doctor.name
            representation['doctor_specialists'] = [specialist.specialist_name for specialist in instance.doctor.specialists.all()]
            representation['doctor_specialists_bn'] = [specialist.specialist_name_bn for specialist in instance.doctor.specialists.all()]

        # Serialize the chamber object
        if instance.chamber:
            chamber_serializer = ChamberSerializer(instance.chamber)
            representation['chamber'] = chamber_serializer.data

        return representation

        
class TestAppointmentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=TestAppointment
        fields = "__all__"
        extra_kwargs = {
            'appointment_id': {'read_only': True},
            'fee': {'required': False},
            'comment': {'required': False},
        }
    def create(self, validated_data):
        test_id = validated_data['test'].id
        user_id = validated_data['user'].id
        hospital_id = validated_data['hospital'].id
        date = validated_data['date'].strftime('%Y%m%d')
        time = validated_data['time'].strftime('%H%M')
        
        # Generate appointment_id based on specified format
        validated_data['appointment_id'] = f"{test_id}{hospital_id}{date}{time}{user_id}"
        
        # Set fee from hospital.fee
        validated_data['fee'] = validated_data['test'].fee
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Serialize the user object
        if instance.user:
            representation['user_id'] = instance.user.id
            representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"

        # Serialize the test object
        if instance.test:
            representation['test_id'] = instance.test.id
            representation['test'] = instance.test.test_name

        # Serialize the hospital object
        if instance.hospital:
            representation['hospital_id'] = instance.hospital.id
            representation['hospital'] = instance.hospital.name
            representation['hospital_availability'] = instance.hospital.availability
            
            address = instance.hospital.address
            location = instance.hospital.location
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""

            representation["hospital_address"] = ", ".join(filter(None, [address, upazila_name, district_name, division_name]))

        return representation

    


from rest_framework import serializers
from .models import  AppointmentInfo
import random
import string
from drf_extra_fields.fields import Base64FileField
import filetype

class Base64FileField(Base64FileField):
    """
    A custom serializer field to handle base64-encoded files.
    """
    ALLOWED_MIME_TYPES = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'application/pdf': 'pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    }

    ALLOWED_TYPES = ['pdf', 'docx', 'jpg', 'jpeg', 'png']

    def get_file_extension(self, filename, decoded_file):
        extension = filetype.guess_extension(decoded_file)
        return extension

    def to_internal_value(self, data):
        if isinstance(data, str):
            return super().to_internal_value(data)
        return data


class AppointmentInfoSerializer(serializers.ModelSerializer):
    file_upload = Base64FileField()
    class Meta:
        model = AppointmentInfo
        fields = "__all__"
