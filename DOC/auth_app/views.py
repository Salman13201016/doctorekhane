from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rest_framework.views import APIView  
from django.contrib.sessions.models import Session
from rest_framework.authtoken.models import Token   
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# dj rest auth
from dj_rest_auth.views import LoginView
from django.utils.crypto import get_random_string
# model
from user.models import Profile
from doctor.models import Doctor
from hospital.models import Hospital
# from django.contrib.auth.models import User
from user.models import User
from .models import OTP
# serializer
from .serializers import UserRegistrationSerializer,DoctorRegistrationSerializer,HospitalRegistrationSerializer
from DOC.settings import DEFAULT_FROM_EMAIL
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserRegistrationView(viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            subject = 'Welcome To DOC'
            message = f"Dear {request.data['first_name']},\n\nWelcome to DOC – Your Comprehensive Medical Companion!\n\nWe are delighted to have you on board. With DOC, you gain access to a wealth of information about hospitals, doctors, ambulances, and more, all at your fingertips.\n\nWhether you're seeking the right healthcare professional, need emergency assistance, or simply want to stay informed about medical facilities in your area, DOC is here to simplify your healthcare journey.\n\nFeel free to explore the platform and discover the range of features designed to make your healthcare experience seamless. If you have any questions or need assistance, our support team is ready to help.\n\nThank you for choosing DOC. We look forward to being your trusted partner in health.\n\nBest regards,\nThe DOC Team"
            from_email = DEFAULT_FROM_EMAIL
            to_email = request.data["email"]
            send_mail(subject, message, from_email, [to_email], fail_silently=True)
            return Response({"message":"account created successfully"} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            user = self.request.data.get('user')

            if not user:
                raise ValueError({"message": "Phone number or email is required for login."})

            profile = None
            if "@" in user:
                profile = Profile.objects.get(user__email=user)
            else:
                profile = Profile.objects.get(phone_number=user)
            self.request.data['username'] = profile.user.username
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()

            # Include profile_image in the response
            response_data = {
                "access": self.get_response().data['access'],
                "refresh": self.get_response().data['refresh'],
                "user": {
                    "pk": profile.user.pk,
                    "username": profile.user.username,
                    "email": profile.user.email,
                    "first_name": profile.user.first_name,
                    "last_name": profile.user.last_name,
                    "role" : profile.user.role,
                    "is_superuser" : profile.user.is_superuser,
                    "profile" : {
                        "phone_number" : profile.phone_number,
                        "profile_image": request.build_absolute_uri(profile.profile_image.url) if profile.profile_image else None,
                    },
                }
            }
            return Response(response_data)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Unable to log in with provided credentials."}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class DoctorRegistrationView(viewsets.GenericViewSet):
    serializer_class = DoctorRegistrationSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # subject = 'Welcome To DOC'
            # message = f"Dear {request.data['first_name']},\n\nWelcome to DOC – Your Comprehensive Medical Companion!\n\nWe are delighted to have you on board. With DOC, you gain access to a wealth of information about hospitals, doctors, ambulances, and more, all at your fingertips.\n\nWhether you're seeking the right healthcare professional, need emergency assistance, or simply want to stay informed about medical facilities in your area, DOC is here to simplify your healthcare journey.\n\nFeel free to explore the platform and discover the range of features designed to make your healthcare experience seamless. If you have any questions or need assistance, our support team is ready to help.\n\nThank you for choosing DOC. We look forward to being your trusted partner in health.\n\nBest regards,\nThe DOC Team"
            # from_email = DEFAULT_FROM_EMAIL
            # to_email = request.data["email"]
            # send_mail(subject, message, from_email, [to_email], fail_silently=True)
            return Response({"message":"account created successfully"} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            user = self.request.data.get('user')

            if not user:
                raise ValueError({"message": "Phone number or email is required for login."})

            doctor = None
            if "@" in user:
                doctor = Doctor.objects.get(user__email=user,profile=True)
            else:
                doctor = Doctor.objects.get(phone_number=user,profile=True)
            self.request.data['username'] = doctor.user.username
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()

            # Include profile_image in the response
            response_data = {
                "access": self.get_response().data['access'],
                "refresh": self.get_response().data['refresh'],
                "user": {
                    "pk": doctor.user.pk,
                    "username": doctor.user.username,
                    "email": doctor.user.email,
                    "first_name": doctor.user.first_name,
                    "last_name": doctor.user.last_name,
                    "role" : doctor.user.role,
                    "is_superuser" : doctor.user.is_superuser,
                    "profile" : {
                        "phone_number" : doctor.phone_number,
                        "profile_image": request.build_absolute_uri(doctor.profile_image.url) if doctor.profile_image else None,
                    },
                }
            }
            return Response(response_data)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Unable to log in with provided credentials."}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class HospitalRegistrationView(viewsets.GenericViewSet):
    serializer_class = HospitalRegistrationSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # subject = 'Welcome To DOC'
            # message = f"Dear {request.data['first_name']},\n\nWelcome to DOC – Your Comprehensive Medical Companion!\n\nWe are delighted to have you on board. With DOC, you gain access to a wealth of information about hospitals, doctors, ambulances, and more, all at your fingertips.\n\nWhether you're seeking the right healthcare professional, need emergency assistance, or simply want to stay informed about medical facilities in your area, DOC is here to simplify your healthcare journey.\n\nFeel free to explore the platform and discover the range of features designed to make your healthcare experience seamless. If you have any questions or need assistance, our support team is ready to help.\n\nThank you for choosing DOC. We look forward to being your trusted partner in health.\n\nBest regards,\nThe DOC Team"
            # from_email = DEFAULT_FROM_EMAIL
            # to_email = request.data["email"]
            # send_mail(subject, message, from_email, [to_email], fail_silently=True)
            return Response({"message":"account created successfully"} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            user = self.request.data.get('user')

            if not user:
                raise ValueError({"message": "Phone number or email is required for login."})

            hospital = None
            if "@" in user:
                hospital = Hospital.objects.get(user__email=user,profile=True)
            else:
                hospital = Hospital.objects.get(phone_number=user,profile=True)
            self.request.data['username'] = hospital.user.username
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()

            # Include profile_image in the response
            response_data = {
                "access": self.get_response().data['access'],
                "refresh": self.get_response().data['refresh'],
                "user": {
                    "pk": hospital.user.pk,
                    "username": hospital.user.username,
                    "email": hospital.user.email,
                    "first_name": hospital.user.first_name,
                    "role" : hospital.user.role,
                    "is_superuser" : hospital.user.is_superuser,
                    "profile" : {
                        "phone_number" : hospital.phone_number,
                        "profile_image": request.build_absolute_uri(hospital.hospital_image.url) if hospital.hospital_image else None,
                    },
                }
            }
            return Response(response_data)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Unable to log in with provided credentials."}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'message': 'phone_number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(profile__phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate and save OTP using the OTP model
        otp = "123456"
        otp_obj, created = OTP.objects.get_or_create(phone_number=phone_number)
        otp_obj.otp = otp
        otp_obj.save()

        # Send OTP via your preferred method (e.g., SMS)

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    
class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp_value = request.data.get('otp')

        if not phone_number or not otp_value:
            return Response({'message': 'Phone number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(profile__phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve OTP from the OTP model
        try:
            otp_obj = OTP.objects.get(phone_number=phone_number)
            stored_otp = otp_obj.otp
        except OTP.DoesNotExist:
            return Response({'message': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not stored_otp or otp_value != stored_otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate and return token
        token, created = Token.objects.get_or_create(user=user)

        # Clear the OTP from the OTP model after successful verification
        otp_obj.delete()

        return Response({'message': 'Verification successful', 'token': token.key}, status=status.HTTP_200_OK)
    
class UpdatePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        token_key = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not token_key or not new_password or not confirm_password:
            return Response({'message': 'Token and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()

        # Invalidate the old token
        token.delete()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    

class SendOTPViewReg(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'message': 'phone_number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # otp = get_random_string(length=6, allowed_chars='1234567890')
        # Generate and save OTP using the OTP model
        otp = "123456"
        otp_obj, created = OTP.objects.get_or_create(phone_number=phone_number)
        otp_obj.otp = otp
        otp_obj.save()

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    

class VerifyOTPViewReg(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp_value = request.data.get('otp')

        if not phone_number or not otp_value:
            return Response({'message': 'phone_number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve OTP from the OTP model
        try:
            otp_obj = OTP.objects.get(phone_number=phone_number)
            stored_otp = otp_obj.otp
        except OTP.DoesNotExist:
            return Response({'message': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not stored_otp or otp_value != stored_otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Clear the OTP from the session after successful verification
        otp_obj.delete()

        return Response({"message":"OTP Verified"}, status=status.HTTP_200_OK)

from dj_rest_auth.serializers import PasswordChangeSerializer
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

sensitive_post_parameters_m = method_decorator(sensitive_post_parameters('password', 'old_password', 'new_password1', 'new_password2',),) 

class PasswordChangeView(GenericAPIView):

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'New password has been saved.'}, status=status.HTTP_200_OK)
        default_errors = serializer.errors
        err_message = ''
        for field_name, field_errors in default_errors.items():
            if err_message != '':
                err_message += ' '
            err_message += field_errors[0]
            
        return Response({"message" : err_message}, status=status.HTTP_400_BAD_REQUEST)

# auth
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

'''
Social authjentecation
'''

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
