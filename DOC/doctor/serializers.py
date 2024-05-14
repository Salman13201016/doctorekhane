from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Q
from hospital.models import Hospital
from .models import Doctor, Chamber , DoctorService , Experience, Review
from appointment.models import DoctorAppointment
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
        hospital_name = attrs.get('hospital') if attrs.get('hospital') else None
        # Check if the hospital has profile set to False
        hospital_has_profile = Hospital.objects.filter(name=hospital_name, profile=False).exists()
        if hospital_name is not None:
            if hospital_has_profile:
                if self.instance:
                    # If updating an existing instance
                    if Chamber.objects.filter(Q(availability=attrs.get('availability'), hospital__name=attrs.get('hospital')) | Q(availability_bn=attrs.get('availability_bn'), hospital__name=attrs.get('hospital'))
                        ).exclude(id=self.instance.id).exists():
                        raise serializers.ValidationError({"message": 'Same Chamber Time already exists'})
                else:
                    # If creating a new instance
                    if Chamber.objects.filter( Q(availability=attrs.get('availability'), hospital__name=attrs.get('hospital')) | Q(availability_bn=attrs.get('availability_bn'), hospital__name=attrs.get('hospital'))).exists():
                        raise serializers.ValidationError({"message": 'Same Chamber Time already exists'})
            else:
                raise serializers.ValidationError({"message": 'This is not a valid chamber'})
        else:
            if self.instance:
                # If updating an existing instance
                if Chamber.objects.filter(Q(name=attrs.get('name'), availability=attrs.get('availability')) | Q(name_bn=attrs.get('name_bn'), availability_bn=attrs.get('availability_bn'))
                    ).exclude(id=self.instance.id).exists():
                        raise serializers.ValidationError({"message": 'Same Chamber Time already exists'})
                else:
                    # If creating a new instance
                    if Chamber.objects.filter(Q(name=attrs.get('name'), availability=attrs.get('availability')) | Q(name_bn=attrs.get('name_bn'), availability_bn=attrs.get('availability_bn')) ).exists():
                        raise serializers.ValidationError({"message": 'Same Chamber Time already exists'})
        return super().validate(attrs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.personal:
            data["hospital_id"] = instance.hospital.id if instance.hospital else None
            data["chamber_name"] = instance.hospital.name if instance.hospital else None
            data["chamber_address"] = instance.hospital.address if instance.hospital else None
            del data["hospital"]
            del data["name"]
            del data["name_bn"]
            del data["address"]
            del data["address_bn"]
        else:
            data["chamber_name"] = instance.name
            data["chamber_name_bn"] = instance.name_bn
            data["chamber_address"] = instance.address
            data["chamber_address_bn"] = instance.address_bn
            del data["hospital"]
            del data["name"]
            del data["name_bn"]
            del data["address"]
            del data["address_bn"]

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
            # If updating an existing instance
            if Experience.objects.filter(
                (Q(working_place__iexact=attrs.get('working_place')) |
                Q(working_place_bn__iexact=attrs.get('working_place_bn'))) &
                Q(doctor=attrs.get('doctor'))
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Doctor with the same working place experience already exists'})
        else:
            # If creating a new instance
            if Experience.objects.filter(
                Q(working_place__iexact=attrs.get('working_place')) |
                Q(working_place_bn__iexact=attrs.get('working_place_bn')),
                doctor=attrs.get('doctor')
            ).exists():
                raise serializers.ValidationError({"message": 'Doctor with the same working place experience already exists'})

    
class DoctorServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = DoctorService
        fields = "__all__"
        extra_kwargs = {
            'id' : {'read_only': False},
        }

    # def validate(self, attrs):
    #     if self.instance:
    #         if DoctorService.objects.filter(service_name__iexact=attrs.get('service_name')).exclude(id=self.instance.id).exists():
    #             raise serializers.ValidationError({"message": 'Doctor With Same Service already exists'})
    #     elif DoctorService.objects.filter(service_name__iexact=attrs.get('service_name')).exists():
    #         raise serializers.ValidationError({"message": 'Doctor With Same Service already exists'})
    #     return attrs

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
             'title' : { 'required': True },
             'nid' : { 'required': True },
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
        specialists = []
        for specialist_id in specialist_ids:
            specialist = Specialist.objects.filter(id=specialist_id).first()
            if specialist:
                specialists.append({"id": specialist.id,"name": specialist.specialist_name ,"name_bn": specialist.specialist_name_bn})
        data['specialist'] = specialists
        data['reviews'] = list(Review.objects.filter(doctor=instance.id).values("user__first_name","user__last_name","created_at","content","rating"))

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
        if services_data is not None:
            instance.services.clear()
        if 'specialists' in doctor_data:
            instance.doctor.specialists.set(doctor_data.pop('specialists'))

        # Update doctor fields
        for attr, value in doctor_data.items():
            setattr(instance.doctor, attr, value)
        
        # Set location ID to the Doctor instance's location field
        # instance.doctor.location = doctor_data.get('location')

        # Save doctor instance
        instance.doctor.save()
        # Update related chamber
        if chambers_data is not None:
            for chamber_data in chambers_data:
                chamber_id = chamber_data.get('id')
                if chamber_id:
                    # Update existing experience
                    chamber_instance = instance.doctor.chamber.filter(doctor=instance.doctor,id=chamber_id).first()
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
                    experience_instance = instance.doctor.experiences.filter(doctor=instance.doctor,id=experience_id).first()
                    if experience_instance:
                        for attr, value in experience_data.items():
                            setattr(experience_instance, attr, value)
                        experience_instance.save()
                else:
                    # Create new experience
                    Experience.objects.create(doctor=instance.doctor, **experience_data)

        # Update related services
        if services_data:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    service_instance = DoctorService.objects.filter(id=service_id).first()
                    if service_instance:
                        # Update service instance attributes
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    service_instance, _ = DoctorService.objects.get_or_create(service_name=service_data.get("service_name"))
                instance.services.add(service_instance)

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
        data['reviews'] = list(Review.objects.filter(doctor=instance.id).values("user__first_name","user__last_name","created_at","content","rating"))
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
             'license_no_bn' : { 'required': True }, 
             'specialists' : { 'required': True }, 
             'qualification' : { 'required': True }, 
             'qualification_bn' : { 'required': True }, 
             'phone_number' : { 'required': True }, 
             'email' : { 'required': True }, 
             'slug': {'read_only': True},
             'slug_bn': {'read_only': True},
        }
    def validate(self , attrs):
        if self.instance:
            # If updating an existing instance
            if Doctor.objects.filter(
                (Q(license_no__iexact=attrs.get('license_no')) |
                Q(license_no_bn__iexact=attrs.get('license_no_bn'))) &
                Q(profile=False)
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'License number already exists'})
        else:
            # If creating a new instance
            if Doctor.objects.filter(
                Q(license_no__iexact=attrs.get('license_no')) |
                Q(license_no_bn__iexact=attrs.get('license_no_bn')),
                profile=False
            ).exists():
                raise serializers.ValidationError({"message": 'License number already exists.'})

        if self.instance:
            if  Doctor.objects.filter(profile=False,phone_number__iexact=attrs.get('phone_number')).exclude(id=self.instance.id).exists():
                        raise serializers.ValidationError({"message": 'Phone Number already exists'})
        elif Doctor.objects.filter(profile=False,phone_number__iexact=attrs.get('phone_number')).exists():
            raise serializers.ValidationError({"message": 'Phone Number already exists.'})
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
            service_instance, _ = DoctorService.objects.get_or_create(service_name=service_data.get("service_name"),service_name_bn=service_data.get("service_name_bn"))
            doctor.services.add(service_instance)

        return doctor

    def update(self, instance, validated_data):
        chambers_data = validated_data.pop('chamber', None)
        experiences_data = validated_data.pop('experiences', None)
        services_data = validated_data.pop('services', None)
        if services_data is not None:
            instance.services.clear()

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

        if services_data:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    service_instance = DoctorService.objects.filter(id=service_id).first()
                    if service_instance:
                        # Update service instance attributes
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    # Try to get the instance based on service_name
                    service_instance, created = DoctorService.objects.get_or_create(
                        service_name=service_data.get("service_name")
                    )

                    # If not found, try to get the instance based on service_name_bn
                    if not service_instance:
                        service_instance, created = DoctorService.objects.get_or_create(
                            service_name_bn=service_data.get("service_name_bn")
                        )

                instance.services.add(service_instance)


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
        specialists = []
        for specialist_id in specialist_ids:
            specialist = Specialist.objects.filter(id=specialist_id).first()
            if specialist:
                specialists.append({"id": specialist.id,"name": specialist.specialist_name,"name_bn": specialist.specialist_name_bn})
        data['specialist'] = specialists
        data['reviews'] = list(Review.objects.filter(doctor=instance.id).values("user__first_name","user__last_name","created_at","content","rating"))
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # read_only_fields = ('user',)
        lookup_fields = ['product']

    def validate(self, attrs):
        appointment = attrs.get('appointment')
        doctor = attrs.get('doctor')

        
        if self.instance:
            return attrs

        if not DoctorAppointment.objects.filter(id=appointment.id, doctor=doctor).exists():
            raise serializers.ValidationError({"message":"You haven't appointment this doctor yet."})
        
        if Review.objects.filter(appointment=appointment, doctor=doctor).exists():
            raise serializers.ValidationError({"message":"You have already written a review for this doctor."})
    
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        # Prevent updating the user and order fields
        validated_data.pop('user', None)
        validated_data.pop('appointment', None)

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        representation['appointment'] = instance.appointment.appointment_id 
        representation['doctor'] = instance.doctor.name   
        return representation
