from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
#model
from .models import FAQ, ActionLog, Divisions, Districts, Goal, Notice, Notifications, OthersContent, SiteSettings, Team, Upazilas,Services,Specialist

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisions
        fields = "__all__"

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = "__all__"

class UpazilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upazilas
        fields = "__all__"


class SpecialistSerializer(serializers.ModelSerializer):
    specialist_logo = Base64ImageField(required=False,allow_null=True)
    class Meta:
        model = Specialist
        fields = "__all__"
        extra_kwargs = {
            'slug':{'required':False},
            'slug_bn':{'required':False},
        }
        def validate(self , attrs):
            if self.instance:
                if  Specialist.objects.filter(Q(specialist_name__iexact=attrs.get('specialist_name')) | Q(specialist_name_bn__iexact=attrs.get('specialist_name_bn'))).exclude(id=self.instance.id).exists():
                            raise serializers.ValidationError({"message": 'Specialist Name already exists'})
            elif Specialist.objects.filter(Q(specialist_name__iexact=attrs.get('specialist_name')) | Q(specialist_name_bn__iexact=attrs.get('specialist_name_bn'))).exists():
                raise serializers.ValidationError({"message": 'Specialist Name already exists.'})
            return attrs

from django.db.models import Q
class ServicesSerializer(serializers.ModelSerializer):
    service_logo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Services
        fields ="__all__"
        extra_kwargs = {
            'slug':{'required':False},
            'slug_bn':{'required':False},
        }

    def validate(self, attrs):
        if self.instance:
            if Services.objects.filter(Q(service_name__iexact=attrs.get('service_name')) | Q(service_name_bn__iexact=attrs.get('service_name_bn'))).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Service already exists.'})
            
        elif Services.objects.filter(Q(service_name__iexact=attrs.get('service_name')) | Q(service_name_bn__iexact=attrs.get('service_name_bn'))).exists():
            raise serializers.ValidationError({"message": 'Service Name already exists.'})
        return attrs

class TeamSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Team
        fields = "__all__"


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(required=False, allow_null=True)
    banner = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = SiteSettings
        fields ="__all__"
        extra_kwargs = {
            'logo':{'required':False},
            'banner':{'required':False},
            'phone':{'required':False},
            'mail':{'required':False},
            'whatsapp':{'required':False},
        }


class ActionLogSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ActionLog
        fields = '__all__'

    def to_representation(self, instance):

        data = super().to_representation(instance) 
        return data
    
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = "__all__"
    
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"

class GoalSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Goal
        fields ="__all__"

    def validate(self, attrs):
        if self.instance:
            if Goal.objects.filter(Q(title__iexact=attrs.get('title')) | Q(title_bn__iexact=attrs.get('title_bn'))).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Title already exists.'})
            
        elif Goal.objects.filter(Q(title__iexact=attrs.get('title')) | Q(title_bn__iexact=attrs.get('title_bn'))).exists():
            raise serializers.ValidationError({"message": 'Title already exists.'})
        return attrs
    
class OthersContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OthersContent
        fields ="__all__"
 
class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields ="__all__"

                