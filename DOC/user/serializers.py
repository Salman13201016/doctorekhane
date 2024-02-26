import random
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.core.mail import send_mail
from DOC.settings import DEFAULT_FROM_EMAIL

# model
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

#serializer

import random
import string

def generate_random_password():
    """Generate a random password string."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

'''
Nested Seria;izser
'''
# 👇 01. ProfileSerializer 
class ProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Profile
        fields = "__all__" 
        extra_kwargs = {
            'phone_number' : {'required': True},
            'user' : {'read_only': True},
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = instance.profile_image.url

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
    

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'profile']
        extra_kwargs = {
            'username' : {'read_only': True},
            'is_superuser' : {'read_only': True},
        }
    def validate(self, attrs):
        profile = attrs.get('profile', None)
        if self.instance:
            if "role" in profile:
                raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
                
        if self.instance and User.objects.filter(email=attrs.get('email')).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})
        elif not self.instance and User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})
        
        if profile:
            phone_number = profile.get('phone_number')
            if self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exclude(id=self.instance.profile.id).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
            elif not self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
        return super().validate(attrs)
        
    
    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            for item, value in validated_data.pop('profile').items():
                setattr(instance.profile, item, value)
            
            instance.profile.save()
            # userProfile =  Profile.objects.filter(user=instance).update(**validated_data.pop('profile'))
        
        # update user
        for item, value in validated_data.items():
            setattr(instance, item, value)
        instance.save()
        
        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.hospital_image.url)

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
    

class UserManagementSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'profile']
        extra_kwargs = {
            'first_name' : {'required': True},
            'last_name' : {'required': True},
            'username' : {'read_only': True},
            'is_superuser' : {'read_only': True},
        }

    def validate(self, attrs):
        profile = attrs.get('profile', None)
        if "role" in profile:
            raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
        if self.instance:
            if self.instance.profile.role == "admin":
                raise serializers.ValidationError({"message": 'You are not authorised to do this action'})
        
        if self.instance and User.objects.filter(email=attrs.get('email')).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})
        elif not self.instance and User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})
        
        if profile:
            phone_number = profile.get('phone_number')
            if self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exclude(id=self.instance.profile.id).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
            elif not self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        # user and profile data
        request = self.context.get('request')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = generate_random_password()
        getProfileInfo = validated_data.pop('profile')
        
        random_number = random.randint(100000, 999999)
        username = first_name+last_name+str(random_number)
        user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
        subject = 'Welcome To Doctor Ekhane',
        message =(
                f'Dear {user.first_name}'
                f'\nYour username is {user.username}'
                f'\nYour temporary password is {password}, please change it after login.'
                )
        from_email = DEFAULT_FROM_EMAIL
        to_email = request.data["email"]
        send_mail(subject, message, from_email, [to_email], fail_silently=True)
       
        if created:
            user.set_password(password)

        for item, value in getProfileInfo.items():
            setattr(user.profile, item, value)

        user.save()
        user.profile.save()     
        
        return user

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            for item, value in validated_data.pop('profile').items():
                setattr(instance.profile, item, value)
            
            instance.profile.save()
            # userProfile =  Profile.objects.filter(user=instance).update(**validated_data.pop('profile'))
        
        # update user
        for item, value in validated_data.items():
            setattr(instance, item, value)
        instance.save()
        
        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.hospital_image.url)

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


class SuperUserManagementSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'profile']
        extra_kwargs = {
            'first_name' : {'required': True},
            'last_name' : {'required': True},
            'username' : {'read_only': True},
            'is_superuser' : {'read_only': True},
        }

    def validate(self, attrs):
        profile = attrs.get('profile', None)
        if self.instance and User.objects.filter(email=attrs.get('email')).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})
        elif not self.instance and User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists'})

        if profile:
            phone_number = profile.get('phone_number')
            if self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exclude(id=self.instance.profile.id).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
            elif not self.instance and phone_number and Profile.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        # user and profile data
        request = self.context.get('request')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        role = validated_data.pop('role')
        password = generate_random_password()
        getProfileInfo = validated_data.pop('profile')
        
        random_number = random.randint(100000, 999999)
        username = first_name+last_name+str(random_number)
        user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
        subject = 'Welcome To DOC',
        message =(
                f'Dear {user.first_name}'
                f'\nYour username is {user.username}'
                f'\nYour temporary password is {password}, please change it after login.'
                )
        from_email = DEFAULT_FROM_EMAIL
        to_email = request.data["email"]
        send_mail(subject, message, from_email, [to_email], fail_silently=True)
        
        if created:
            if role == "superadmin":
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
            user.set_password(password)
        for item, value in getProfileInfo.items():
            setattr(user.profile, item, value)

        user.save()
        user.profile.save()     
        
        return user


    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            for item, value in profile_data.items():
                setattr(instance.profile, item, value)

            instance.profile.save()

            # Check if 'role' is in the profile data
            role = profile_data.get('role', instance.profile.role if instance.profile else None)
            if role == "superadmin":
                instance.is_superuser = True
                instance.is_staff = True
        # update user
        for item, value in validated_data.items():
            setattr(instance, item, value)

        instance.save()

        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = request.build_absolute_uri(instance.hospital_image.url)

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

class DonorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name']

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        address = instance.profile.address
        location = instance.profile.location

        union_name = location.union_name if location else ""
        upazila_name = location.upazila.upazila_name if location and location.upazila else ""
        district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
        division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
        
        data['Profile Image'] = request.build_absolute_uri(instance.profile.profile_image.url) if instance.profile.profile_image else None
        data['Blood Group'] = instance.profile.blood_group
        data['Phone Number'] = instance.profile.phone_number
        data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
        
        return data