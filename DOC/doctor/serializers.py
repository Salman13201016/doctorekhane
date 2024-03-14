from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Doctor, Chamber , DoctorService , Experience
from app.models import Specialist
# from django.contrib.auth.models import User
from user.models import User
from django.core.mail import send_mail
from DOC.settings import DEFAULT_FROM_EMAIL
import random
import string

def generate_random_password():
    """Generate a random password string."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

class ChamberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Chamber
        exclude = ["doctor"]
        extra_kwargs = {
            'id' : {'read_only': False},
        }

    def validate(self, attrs):
        if self.instance:
            if Chamber.objects.filter(hospital__name=attrs.get('hospital'), doctor=attrs.get('doctor')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Doctor With Same Chamber already exists'})
        elif Chamber.objects.filter(hospital__name=attrs.get('hospital'), doctor=attrs.get('doctor')).exists():
            raise serializers.ValidationError({"message": 'Doctor With Same Chamber already exists'})
        return attrs
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["hospital_name"] = instance.hospital.name if instance.hospital else None
        data["hospital_address"] = instance.hospital.address if instance.hospital else None
        del data["hospital"]
        return data

class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Experience
        exclude = ["doctor"]
        extra_kwargs = {
            'id' : {'read_only': False},
        }

    def validate(self, attrs):
        if self.instance:
            if Experience.objects.filter(working_place__iexact=attrs.get('working_place'), doctor=attrs.get('doctor')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Doctor With Same Working Place Experience already exists'})
        elif Experience.objects.filter(working_place__iexact=attrs.get('working_place'), doctor=attrs.get('doctor')).exists():
            raise serializers.ValidationError({"message": 'Doctor With Same Working Place Experience already exists'})
        return attrs
    
class DoctorServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = DoctorService
        exclude = ["doctor"]
        extra_kwargs = {
            'id' : {'read_only': False},
        }

    def validate(self, attrs):
        if self.instance:
            if DoctorService.objects.filter(service_name__iexact=attrs.get('service_name'), doctor=attrs.get('doctor')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Doctor With Same Service already exists'})
        elif DoctorService.objects.filter(service_name__iexact=attrs.get('service_name'), doctor=attrs.get('doctor')).exists():
            raise serializers.ValidationError({"message": 'Doctor With Same Service already exists'})
        return attrs

class DoctorProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False,allow_null=True)
    chamber = ChamberSerializer(required = False, allow_null = True, many = True)
    experiences = ExperienceSerializer(required = False, allow_null = True, many = True)
    services = DoctorServiceSerializer(required = False, allow_null = True, many = True)
    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
             'license_no' : { 'required': True }, 
             'specialists' : { 'required': True }, 
             'qualification' : { 'required': True }, 
             'phone_number' : { 'required': True }, 
             'email' : { 'required': True }, 
             'slug': {'read_only': True},
             'profile': {'read_only': True},
        }
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        
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

class DoctorProfileManagementSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'doctor']
        extra_kwargs = {
            'username': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def validate(self, attrs):
        doctorProfile = attrs.get('doctor', None)
        if doctorProfile:
            license_no = doctorProfile.get('license_no')
            phone_number = doctorProfile.get('phone_number')

            if self.instance:
                if license_no and Doctor.objects.filter(profile=True,license_no=license_no).exclude(id=self.instance.doctor.id).exists():
                    raise serializers.ValidationError({"message": 'License number already exists'})
                if phone_number and Doctor.objects.filter(profile=True,phone_number=phone_number).exclude(id=self.instance.doctor.id).exists():
                    raise serializers.ValidationError({"message": 'Phone number already exists'})
            else:
                if license_no and Doctor.objects.filter(profile=True,license_no=license_no).exists():
                    raise serializers.ValidationError({"message": 'License number already exists'})
                if phone_number and Doctor.objects.filter(profile=True,phone_number=phone_number).exists():
                    raise serializers.ValidationError({"message": 'Phone number already exists'})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        doctor_data = validated_data.pop('doctor', {})
        chambers_data = doctor_data.pop('chamber', None)
        experiences_data = doctor_data.pop('experiences', None)
        services_data = doctor_data.pop('services', None)
        if 'specialists' in doctor_data:
            instance.doctor.specialists.set(doctor_data.pop('specialists'))

        # Update doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save doctor instance
        instance.save()
        # Update related chamber
        if chambers_data is not None:
            for chamber_data in chambers_data:
                chamber_id = chamber_data.get('id')
                if chamber_id:
                    # Update existing experience
                    chamber_instance = instance.chamber.filter(doctor=instance.doctor,id=chamber_id).first()
                    if chamber_instance:
                        for attr, value in chamber_data.items():
                            setattr(chamber_instance, attr, value)
                        chamber_instance.save()
                else:
                    # Create new experience
                    Chamber.objects.create(doctor=instance.doctor, **chamber_data)

        # Update related experiences
        if experiences_data is not None:
            for experience_data in experiences_data:
                experience_id = experience_data.get('id')
                if experience_id:
                    # Update existing experience
                    experience_instance = instance.experiences.filter(doctor=instance.doctor,id=experience_id).first()
                    if experience_instance:
                        for attr, value in experience_data.items():
                            setattr(experience_instance, attr, value)
                        experience_instance.save()
                else:
                    # Create new experience
                    Experience.objects.create(doctor=instance.doctor, **experience_data)

        # Update related services
        if services_data is not None:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    # Update existing service
                    service_instance = instance.services.filter(doctor=instance.doctor,id=service_id).first()
                    if service_instance:
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    # Create new service
                    DoctorService.objects.create(doctor=instance.doctor, **service_data)

        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        
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
        return data


class DoctorManagementSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False,allow_null=True)
    chamber = ChamberSerializer(required = False, allow_null = True, many = True)
    experiences = ExperienceSerializer(required = False, allow_null = True, many = True)
    services = DoctorServiceSerializer(required = False, allow_null = True, many = True)
    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
             'license_no' : { 'required': True }, 
             'specialists' : { 'required': True }, 
             'qualification' : { 'required': True }, 
             'phone_number' : { 'required': True }, 
             'email' : { 'required': True }, 
             'slug': {'read_only': True},
        }
        def validate(self , attrs):
            if self.instance:
                if  Doctor.objects.filter(profile=False,license_no__iexact=attrs.get('license_no')).exclude(id=self.instance.id).exists():
                            raise serializers.ValidationError({"message": 'License No already exists'})
            elif Doctor.objects.filter(profile=False,license_no__iexact=attrs.get('license_no')).exists():
                raise serializers.ValidationError({"message": 'License No already exists.'})
            return attrs
        
    def create(self, validated_data):
        getchamberInfo = validated_data.pop('chamber', [])
        getexperience_detailsInfo = validated_data.pop('experiences', [])
        getdoctor_serviceInfo = validated_data.pop('services', [])
        specialists_data = validated_data.pop('specialists', [])

        doctor = Doctor.objects.create(**validated_data)
        doctor.specialists.set(specialists_data)

        for chamber_data in getchamberInfo:
            Chamber.objects.create(doctor=doctor, **chamber_data)

        for experience_data in getexperience_detailsInfo:
            Experience.objects.create(doctor=doctor, **experience_data)

        for service_data in getdoctor_serviceInfo:
            DoctorService.objects.create(doctor=doctor, **service_data)

        return doctor

    def update(self, instance, validated_data):
        chambers_data = validated_data.pop('chamber', None)
        experiences_data = validated_data.pop('experiences', None)
        services_data = validated_data.pop('services', None)
        if 'specialists' in validated_data:
            instance.specialists.set(validated_data.pop('specialists'))

        # Update doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save doctor instance
        instance.save()
        # Update related chamber
        if chambers_data is not None:
            for chamber_data in chambers_data:
                chamber_id = chamber_data.get('id')
                if chamber_id:
                    # Update existing experience
                    chamber_instance = instance.chamber.filter(doctor=instance,id=chamber_id).first()
                    if chamber_instance:
                        for attr, value in chamber_data.items():
                            setattr(chamber_instance, attr, value)
                        chamber_instance.save()
                else:
                    # Create new experience
                    Chamber.objects.create(doctor=instance, **chamber_data)

        # Update related experiences
        if experiences_data is not None:
            for experience_data in experiences_data:
                experience_id = experience_data.get('id')
                if experience_id:
                    # Update existing experience
                    experience_instance = instance.experiences.filter(doctor=instance,id=experience_id).first()
                    if experience_instance:
                        for attr, value in experience_data.items():
                            setattr(experience_instance, attr, value)
                        experience_instance.save()
                else:
                    # Create new experience
                    Experience.objects.create(doctor=instance, **experience_data)

        # Update related services
        if services_data is not None:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    # Update existing service
                    service_instance = instance.services.filter(doctor=instance,id=service_id).first()
                    if service_instance:
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    # Create new service
                    DoctorService.objects.create(doctor=instance, **service_data)

        return instance

    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        
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
