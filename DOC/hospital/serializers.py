from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Hospital

class HospitalManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'hospital_image': {'required': False},
            'facilities': {'required': False},
            'services_offered': {'required': False},
            'specialties': {'required': False},
            'accreditation_details': {'required': False},
            'slug': {'required': False},
            'emergency_contact': {'required': False},
            'website': {'required': False},
        }

    def validate(self, data):
        # Check if name already exists
        name = data.get('name')
        if name and (self.instance is None or name != self.instance.name) and Hospital.objects.filter(name=name).exists():
            raise ValidationError({'name': 'Name already exists.'})

        # Check if email already exists
        email = data.get('email')
        if email and (self.instance is None or email != self.instance.email) and Hospital.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email already exists.'})

        # Check if phone_number already exists
        phone_number = data.get('phone_number')
        if phone_number and (self.instance is None or phone_number != self.instance.phone_number) and Hospital.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({'phone_number': 'Phone number already exists.'})

        return data

    def create(self, validated_data):
        """
        Override the create method to set the slug to be the same as the title.
        """
        validated_data['slug'] = validated_data.get('name', '').lower().replace(" ", "-")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override the update method to update the instance and set the slug based on the title.
        """
        for field in self.Meta.model._meta.fields:
            field_name = field.name
            if field_name in validated_data:
                setattr(instance, field_name, validated_data.get(field_name))

        # Set the slug based on the updated title
        instance.slug = instance.name.lower().replace(" ", "-")

        instance.save()
        return instance

class HospitalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['facilities', 'services_offered', 'specialties', 'accreditation_details']

# serializers.py
from rest_framework import serializers
from .models import Hospital

class HospitalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        read_only_fields = ['slug']  # Assuming 'slug' should not be updated directly

