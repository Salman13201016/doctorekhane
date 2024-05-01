from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
#model
from .models import Divisions, Districts, Team, Upazilas,Unions,Services,Specialist

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisions
        fields = ['id', 'division_name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = ['id', 'division','district_name']

class UpazilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upazilas
        fields = ['id','district','upazila_name']

class UnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unions
        fields = ['id','upazila','union_name']

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
                raise serializers.ValidationError({"message": 'Category already exists.'})
            
        elif Services.objects.filter(Q(service_name__iexact=attrs.get('service_name')) | Q(service_name_bn__iexact=attrs.get('service_name_bn'))).exists():
            raise serializers.ValidationError({"message": 'Service Name already exists.'})
        return attrs

class TeamSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Team
        fields = "__all__"
