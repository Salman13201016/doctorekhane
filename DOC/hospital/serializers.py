from rest_framework import serializers
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

from .models import Hospital
from app.models import Services,Specialist
from doctor.models import Chamber

class HospitalManagementSerializer(serializers.ModelSerializer):
    hospital_image = Base64ImageField(required=False,allow_null=True)
    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'hospital_image': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'ac': {'required': False},
            'ambulance_phone_number': {'required': False},
            'slug':{'read_only':True},
            'website': {'required': False},
        }
    def validate(self, attrs):
        # Check if instance exists and if name already exists
        if self.instance:
            if Hospital.objects.filter(name__iexact=attrs.get('name'), address=attrs.get('address')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})
        else:
            if Hospital.objects.filter(name__iexact=attrs.get('name'), address=attrs.get('address')).exists():
                raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})

        # Check if email already exists
        if Hospital.objects.filter(email__iexact=attrs.get('email')).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({'message': 'Email already exists.'})

        # Check if phone_number already exists
        if Hospital.objects.filter(phone_number__iexact=attrs.get('phone_number')).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({'message': 'Phone number already exists.'})

        return attrs
    
    def create(self, validated_data):
        specialists_data = validated_data.pop('specialists', [])
        services_data = validated_data.pop('services', [])

        hospital = Hospital.objects.create(**validated_data)
        hospital.specialists.set(specialists_data)
        hospital.services.set(services_data)

        return hospital

    def update(self, instance, validated_data):
        if 'specialists' in validated_data:
            instance.specialists.set(validated_data.pop('specialists'))
        if 'services' in validated_data:
            instance.services.set(validated_data.pop('services'))

                # Update doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'hospital_image' in data and data['hospital_image']:
            data['hospital_image'] = request.build_absolute_uri(instance.hospital_image.url)

        # Including division, district, and upazila information in the representation
        if 'location' in data and data['location']:
            union = instance.location
            upazila = union.upazila
            district = upazila.district
            division = district.division

            data['location'] = {
                'division': {
                    'id': division.id,
                    'name': division.division_name,
                },
                'district': {
                    'id': district.id,
                    'name': district.district_name,
                },
                'upazila': {
                    'id': upazila.id,
                    'name': upazila.upazila_name,
                },
                'union': {
                    'id': union.id,
                    'name': union.union_name,
                },
            }
        specialist_ids = data.pop('specialists', [])
        specialist_names = []
        for specialist_id in specialist_ids:
            specialist = Specialist.objects.filter(id=specialist_id).first()
            if specialist:
                specialist_names.append(specialist.specialist_name)  # Replace 'specialist_name' with the correct attribute name
        data['specialist'] = specialist_names

        service_ids = data.pop('services', [])
        service_names = []
        for service_id in service_ids:
            services = Services.objects.filter(id=service_id).first()
            if services:
                service_names.append(services.service_name)  # Replace 'specialist_name' with the correct attribute name
        data['service'] = service_names
        data['doctor_count'] = Chamber.objects.filter(hospital=instance).count()
        return data


class AmbulanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id','hospital_image','name', 'ac','ambulance_phone_number']

    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'hospital_image' in data and data['hospital_image']:
            data['hospital_image'] = request.build_absolute_uri(instance.hospital_image.url)
        address = instance.address
        location = instance.location

        union_name = location.union_name if location else ""
        upazila_name = location.upazila.upazila_name if location and location.upazila else ""
        district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
        division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
    
        data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
        
        return data