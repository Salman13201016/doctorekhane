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
        validated_data['fee'] = validated_data['chamber'].fee
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        representation['doctor'] = instance.doctor.name
        representation['doctor_image'] = instance.doctor.name
        representation['doctor_specialists'] = [specialist.specialist_name for specialist in instance.doctor.specialists.all()]

        if not instance.chamber.personal:
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