from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Specialist

class SpecialistSerializer(serializers.ModelSerializer):
    specialist_logo = Base64ImageField(required=False,allow_null=True)
    class Meta:
        model = Specialist
        fields = ['id','specialist_name',"specialist_logo"]
        def validate(self , attrs):
            if self.instance:
                if  Specialist.objects.filter(specialist_name__iexact=attrs.get('specialist_name')).exclude(id=self.instance.id).exists():
                            raise serializers.ValidationError({"message": 'Specialist Name already exists'})
            elif Specialist.objects.filter(specialist_name__iexact=attrs.get('specialist_name')).exists():
                raise serializers.ValidationError({"message": 'Specialist Name already exists.'})
            return attrs
            