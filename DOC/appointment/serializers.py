from rest_framework import serializers
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
        representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        representation['doctor'] = instance.doctor.name
        representation['doctor_image'] = instance.doctor.name
        representation['doctor_specialists'] = [specialist.specialist_name for specialist in instance.doctor.specialists.all()]
        representation['doctor_specialists_bn'] = [specialist.specialist_name_bn for specialist in instance.doctor.specialists.all()]

        if instance.chamber.personal:
            representation['chamber'] = instance.chamber.name 
            representation['chamber_address'] = instance.chamber.address
        else:
            representation['chamber'] = instance.chamber.hospital.name
            address = instance.chamber.hospital.address
            location = instance.chamber.hospital.location
            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
        
            representation["chamber_address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
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
        representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        representation['test'] = instance.test.test_name 
        representation['hospital'] = instance.hospital.name
        address = instance.hospital.address
        location = instance.hospital.location
        union_name = location.union_name if location else ""
        upazila_name = location.upazila.upazila_name if location and location.upazila else ""
        district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
        division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
    
        representation["hospital_address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))

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
