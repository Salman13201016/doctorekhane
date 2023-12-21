from rest_framework import serializers
#model
from .models import Division, District, State

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"

    def validate(self, data):
        # Check if a division with the same name (case-insensitive) already exists
        name = data.get('name', None)
        existing_division = Division.objects.filter(name__iexact=name).exclude(id=self.instance.id if self.instance else None).first()
        # If an existing division with the same name is found, raise a validation error
        if existing_division:
            raise serializers.ValidationError({"error":"A division with this name already exists."})

        return super().validate(data)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

    def validate(self, data):
        # Check if a division with the same name (case-insensitive) already exists
        name = data.get('name', None)
        existing_district = District.objects.filter(name__iexact=name).exclude(id=self.instance.id if self.instance else None).first()
        # If an existing division with the same name is found, raise a validation error
        if existing_district:
            raise serializers.ValidationError({"error":"A district with this name already exists."})
        if "division" in data and not Division.objects.filter(id=data.get("division").id).exists():
            raise serializers.ValidationError({"error": 'Division does not exist.'})
        return super().validate(data)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"
    
    def validate(self, data):
        # Check if a division with the same name (case-insensitive) already exists
        name = data.get('name', None)
        existing_state = State.objects.filter(name__iexact=name).exclude(id=self.instance.id if self.instance else None).first()
        # If an existing division with the same name is found, raise a validation error
        if existing_state:
            raise serializers.ValidationError({"error":"A state with this name already exists."})
        if "division" in data and not Division.objects.filter(id=data.get("division").id).exists():
            raise serializers.ValidationError({"error": 'Division does not exist.'})
        if "district" in data and not District.objects.filter(id=data.get("district").id).exists():
            raise serializers.ValidationError({"error": 'District does not exist.'})
        
        return super().validate(data)
