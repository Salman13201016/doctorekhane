from rest_framework import serializers
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

from .models import Hospital
from doctor.models import Specialist

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
            'slug':{'read_only':True},
            'website': {'required': False},
        }
    def validate(self, attrs):
        # Check if name already exists
        if Hospital.objects.filter(name__iexact=attrs.get('name'), address=attrs.get('address')).exclude(id=self.instance.id).exists():
            raise ValidationError({'message': 'Hospital this address already exists.'})

        # Check if email already exists
        if Hospital.objects.filter(email__iexact=attrs.get('email')).exclude(id=self.instance.id).exists():
            raise ValidationError({'message': 'Email already exists.'})

        # Check if phone_number already exists
        if Hospital.objects.filter(phone_number__iexact=attrs.get('phone_number')).exclude(id=self.instance.id).exists():
            raise ValidationError({'message': 'Phone number already exists.'})
        return attrs
    
    def create(self, validated_data):
        specialists_data = validated_data.pop('specialists', [])
        services_data = validated_data.pop('services', [])

        hospital = Hospital.objects.create(**validated_data)
        hospital.specialists.set(specialists_data)
        hospital.services.set(services_data)

        return hospital

    
    def update(self, instance, validated_data):

        # Update doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'hospital_image' in data and data['hospital_image']:
            data['hospital_image'] = instance.profile_image.url

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
        return data


