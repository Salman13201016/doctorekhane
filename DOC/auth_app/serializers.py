import random, re
from rest_framework import serializers

#django
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

# model
from django.contrib.auth.models import User
from user.models import Profile
from drf_extra_fields.fields import Base64ImageField


'''
This 👇 UserRegistraionSerializer is used opening a user account
by the help of 👇 UserProfileSerializer
'''
class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    profile_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ["phone_number", "profile_image"]


class UserRegistraionSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'profile']
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"message": 'Email already exists.'})
        
        if attrs.get('profile', None).get('phone_number', None):
            if Profile.objects.filter(phone_number=attrs.get('profile', None).get('phone_number', None)).exists():
                raise serializers.ValidationError({"message": 'Phone number already exists.'})
        # 2) validated by django default password validation
        try:
            validate_password(attrs['password'])
            # Additional check for the combination of characters and numbers
            if not re.search(r'[a-zA-Z]+\d+', attrs['password']):
                raise exceptions.ValidationError("Password must contain a combination of letters and numbers.")
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        random_number = random.randint(100000, 999999)

        username = first_name+last_name+str(random_number)

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        for item, value in validated_data.get('profile').items():
            setattr(user.profile, item, value)
        
        user.profile.save()
        return user




