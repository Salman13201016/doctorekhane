from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
#model
from .models import Divisions, Districts, Upazilas,Unions,Services,Specialist

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
        fields = ['id','specialist_name',"specialist_description","specialist_logo"]
        def validate(self , attrs):
            if self.instance:
                if  Specialist.objects.filter(specialist_name__iexact=attrs.get('specialist_name')).exclude(id=self.instance.id).exists():
                            raise serializers.ValidationError({"message": 'Specialist Name already exists'})
            elif Specialist.objects.filter(specialist_name__iexact=attrs.get('specialist_name')).exists():
                raise serializers.ValidationError({"message": 'Specialist Name already exists.'})
            return attrs


class ServicesSerializer(serializers.ModelSerializer):
    service_logo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Services
        fields = ['id', 'service_name','service_description', 'service_logo']

    def validate(self, attrs):
        if self.instance:
            if Services.objects.filter(service_name__iexact=attrs.get('service_name')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": 'Category already exists.'})
            
        elif Services.objects.filter(service_name__iexact=attrs.get('service_name')).exists():
            raise serializers.ValidationError({"message": 'Service Name already exists.'})
        return attrs
