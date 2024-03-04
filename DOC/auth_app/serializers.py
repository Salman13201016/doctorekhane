import random, re
from rest_framework import serializers
from doctor.serializers import DoctorServiceSerializer,ChamberSerializer,ExperienceSerializer
#django
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

# model
# from django.contrib.auth.models import User
from user.models import User
from doctor.models import Doctor
from user.models import Profile
from drf_extra_fields.fields import Base64ImageField


'''
This 👇 UserRegistraionSerializer is used opening a user account
by the help of 👇 UserProfileSerializer
'''
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ["phone_number", "profile_image",'gender']
        extra_kwargs = {
            'phone_number':{'required':True},
            'gender':{'required':True},
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'password', 'profile']
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists.'})
        
        if attrs.get('profile', None).get('phone_number', None):
            if Profile.objects.filter(phone_number=attrs.get('profile', None).get('phone_number', None)).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists.'})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        random_number = random.randint(100000, 999999)

        username = first_name+last_name+str(random_number)

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name,role='general')
        user.set_password(password)
        user.save()
        for item, value in validated_data.get('profile').items():
            setattr(user.profile, item, value)
        
        user.profile.save()
        return user


class UserDoctorSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Doctor
        fields = ["phone_number", "profile_image",'gender',"license_no","specialists","qualification"]
        extra_kwargs = {
             'license_no' : { 'required': True }, 
             'specialists' : { 'required': True }, 
             'qualification' : { 'required': True }, 
             'phone_number' : { 'required': True }, 
             'gender' : { 'required': True }, 
             'slug': {'read_only': True},
        }

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    doctor = UserDoctorSerializer(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'password', 'doctor']
        
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists.'})
        
        if attrs.get('doctor', None).get('phone_number', None):
            if Profile.objects.filter(phone_number=attrs.get('doctor', None).get('phone_number', None)).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists.'})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        random_number = random.randint(100000, 999999)
        doctor_data = validated_data.pop('doctor', {})
        specialists_data = doctor_data.pop('specialists', [])
        

        username = first_name+last_name+str(random_number)

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name,role='doctor')
        user.set_password(password)
        user.save()
        for item, value in doctor_data.items():
            setattr(user.doctor, item, value)
    
        user.doctor.specialists.set(specialists_data)
        user.doctor.save()
        return user
