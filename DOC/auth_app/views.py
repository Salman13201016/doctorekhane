from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# dj rest auth
from dj_rest_auth.views import LoginView
# , PasswordResetConfirmView, PasswordResetView

# model
from user.models import Profile
from django.contrib.auth.models import User

# serializer
from .serializers import UserRegistraionSerializer
from DOC.settings import DEFAULT_FROM_EMAIL

# Create your views here.
class UserRegistraionView(viewsets.GenericViewSet):
    serializer_class = UserRegistraionSerializer
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

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            phone_number = self.request.data.pop('phone_number')
            profile = Profile.objects.get(phone_number=phone_number)
            self.request.data['username'] = profile.user.username
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()
            return self.get_response()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)