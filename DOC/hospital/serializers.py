from rest_framework import serializers
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from user.models import User

from .models import Hospital,Ambulance,Test,TestCatagory
from app.models import Services,Specialist
from doctor.models import Chamber

class TestCatagorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = TestCatagory
        fields = "__all__"
        extra_kwargs = {
            'id' : {'read_only': False},
        }

class TestSerializer(serializers.ModelSerializer):
    catagory = TestCatagorySerializer(required=True)

    class Meta:
        model = Test
        fields = "__all__"

    def validate(self, attrs):
        catagory_data = attrs.get('catagory')
        catagory_name = catagory_data.get('name')
        catagory_instance = TestCatagory.objects.filter(name=catagory_name).first()
        if self.instance:
            if Test.objects.filter(test_name__iexact=attrs.get('test_name'), catagory=catagory_instance).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Test with this catagory already exists.'})
        else:
            if Test.objects.filter(test_name__iexact=attrs.get('test_name'), catagory=catagory_instance).exists():
                raise serializers.ValidationError({'message': 'Test with this catagory already exists.'})
        return attrs

    
    def create(self, validated_data):
        catagory_data = validated_data.pop('catagory')
        catagory_name = catagory_data.get('name')
        catagory_instance, _ = TestCatagory.objects.get_or_create(name=catagory_name)
        
        validated_data['catagory'] = catagory_instance
        return Test.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        catagory_data = validated_data.pop('catagory', None)  # Get catagory data or None if not present
        if catagory_data:
            catagory_id = catagory_data.get('id')
            print(catagory_id)
            if catagory_id:
                catagory_instance = TestCatagory.objects.filter(id=catagory_id).first()
                if catagory_instance:
                    # Update catagory instance attributes
                    for attr, value in catagory_data.items():
                        setattr(catagory_instance, attr, value)
                    catagory_instance.save()
        # Update Test instance attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Retrieve catagory instance
        catagory_instance = instance.catagory
        
        # Add catagory name and ID to the representation
        data['catagory'] = {
            'id': catagory_instance.id,
            'name': catagory_instance.name
        }
        
        return data


class HospitalProfileSerializer(serializers.ModelSerializer):
    hospital_image = Base64ImageField(required=False,allow_null=True)
    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'hospital_image': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'slug':{'read_only':True},
            'website': {'required': False},
        }
    def to_representation(self, instance):
            request = self.context.get("request")
            data = super().to_representation(instance)
            if 'hospital_image' in data and data['hospital_image']:
                data['hospital_image'] = request.build_absolute_uri(instance.hospital_image.url)

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
            specialist_ids = data.pop('specialists', [])
            specialists = []
            for specialist_id in specialist_ids:
                specialist = Specialist.objects.filter(id=specialist_id).first()
                if specialist:
                    specialists.append({"id": specialist.id,"name": specialist.specialist_name})
            data['specialist'] = specialists

            service_ids = data.pop('services', [])
            services = []
            for service_id in service_ids:
                service = Services.objects.filter(id=service_id).first()
                if service:
                    services.append({"id": service.id,"name": service.service_name})  # Replace 'specialist_name' with the correct attribute name
            data['service'] = services
            test_ids = data.pop('tests', [])
            tests = []
            for test_id in test_ids:
                test = Test.objects.filter(id=test_id).first()
                if service:
                    tests.append({"id": test.id,"name": test.test_name})  # Replace 'specialist_name' with the correct attribute name
            data['test'] = tests
            data['doctor_count'] = Chamber.objects.filter(hospital=instance).count()
            return data

class HospitalProfileManagementSerializer(serializers.ModelSerializer):
    hospital = HospitalProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'hospital']
        extra_kwargs = {
            'username': {'read_only': True},
            'is_superuser': {'read_only': True},
        }
    def validate(self, attrs):
        hospitalProfile = attrs.get('hospital', None)
        if hospitalProfile:
            if self.instance:
                if Hospital.objects.filter(profile=True,name__iexact=attrs.get('name'), address=attrs.get('address')).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})
            else:
                if Hospital.objects.filter(profile=True,name__iexact=attrs.get('name'), address=attrs.get('address')).exists():
                    raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})

            if self.instance:
                if Hospital.objects.filter(profile=True,email__iexact=attrs.get('email')).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError({'message': 'Email already exists.'})
            else:
                if Hospital.objects.filter(profile=True,email__iexact=attrs.get('email')).exists():
                    raise serializers.ValidationError({'message': 'Email already exists.'})

            if self.instance:
                if Hospital.objects.filter(profile=True,phone_number__iexact=attrs.get('phone_number')).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError({'message': 'Phone number already exists.'})
            else:
                if Hospital.objects.filter(profile=True,phone_number__iexact=attrs.get('phone_number')).exists():
                    raise serializers.ValidationError({'message': 'Phone number already exists.'})

        return attrs
    
    def update(self, instance, validated_data):
        hospital_data = validated_data.pop('hospital', {})
        if 'specialists' in hospital_data:
            instance.hospital.specialists.set(hospital_data.pop('specialists'))
        if 'services' in hospital_data:
            instance.hospital.services.set(hospital_data.pop('services'))
        if 'tests' in hospital_data:
            instance.hospital.tests.set(hospital_data.pop('tests'))


        # Update hospital fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'hospital_image' in data and data['hospital_image']:
            data['hospital_image'] = request.build_absolute_uri(instance.hospital_image.url)

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

class HospitalManagementSerializer(serializers.ModelSerializer):
    hospital_image = Base64ImageField(required=False,allow_null=True)
    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'hospital_image': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'slug':{'read_only':True},
            'website': {'required': False},
        }
    def validate(self, attrs):
        if self.instance:
            if Hospital.objects.filter(profile=False, name__iexact=attrs.get('name'), address=attrs.get('address')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})
        else:
            if Hospital.objects.filter(profile=False, name__iexact=attrs.get('name'), address=attrs.get('address')).exists():
                raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})

        if self.instance:
            if Hospital.objects.filter(profile=False, email__iexact=attrs.get('email')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Email already exists.'})
        else:
            if Hospital.objects.filter(profile=False, email__iexact=attrs.get('email')).exists():
                raise serializers.ValidationError({'message': 'Email already exists.'})

        if self.instance:
            if Hospital.objects.filter(profile=False, phone_number__iexact=attrs.get('phone_number')).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Phone number already exists.'})
        else:
            if Hospital.objects.filter(profile=False, phone_number__iexact=attrs.get('phone_number')).exists():
                raise serializers.ValidationError({'message': 'Phone number already exists.'})

        return attrs
    
    def create(self, validated_data):
        specialists_data = validated_data.pop('specialists', [])
        services_data = validated_data.pop('services', [])
        tests_data = validated_data.pop('tests', [])

        hospital = Hospital.objects.create(**validated_data)
        hospital.specialists.set(specialists_data)
        hospital.services.set(services_data)
        hospital.tests.set(tests_data)

        return hospital

    def update(self, instance, validated_data):
        if 'specialists' in validated_data:
            instance.specialists.set(validated_data.pop('specialists'))
        if 'services' in validated_data:
            instance.services.set(validated_data.pop('services'))
        if 'tests' in validated_data:
            instance.tests.set(validated_data.pop('tests'))

        # Update hospital fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        if 'hospital_image' in data and data['hospital_image']:
            data['hospital_image'] = request.build_absolute_uri(instance.hospital_image.url)

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
        specialist_ids = data.pop('specialists', [])
        specialists = []
        for specialist_id in specialist_ids:
            specialist = Specialist.objects.filter(id=specialist_id).first()
            if specialist:
                specialists.append({"id": specialist.id,"name": specialist.specialist_name})
        data['specialist'] = specialists

        service_ids = data.pop('services', [])
        services = []
        for service_id in service_ids:
            service = Services.objects.filter(id=service_id).first()
            if service:
                services.append({"id": service.id,"name": service.service_name})  # Replace 'specialist_name' with the correct attribute name
        data['service'] = services
        test_ids = data.pop('tests', [])
        tests = []
        for test_id in test_ids:
            test = Test.objects.filter(id=test_id).first()
            if test:
                tests.append({"id": test.id,"name": test.test_name})  # Replace 'specialist_name' with the correct attribute name
        data['test'] = tests
        data['doctor_count'] = Chamber.objects.filter(hospital=instance).count()
        return data


class AmbulanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = "__all__"
        extra_kwargs = {
            'hospital_name': {'required': False},
            'slug':{'read_only':True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.hospital:
            hospital = Hospital.objects.get(id = instance.hospital_name.id)
            data['hospital_id'] = hospital.id
            data['hospital_name'] = hospital.name
            address = hospital.address
            location = hospital.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
            
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data.pop("location", None)
        else:
            address = instance.address
            location = instance.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
        
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data.pop("location", None)
        return data
    
class AmbulanceManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = "__all__"
        extra_kwargs = {
            'hospital_name': {'required': False},
            'slug':{'read_only':True},
        }

    def validate(self, data):
        if data.get('hospital') and not data.get('hospital_name'):
            raise serializers.ValidationError({"message":"Hospital name cannot be empty if hospital is True."})
        return data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.hospital :# Including division, district, and upazila information in the representation
            hospital = Hospital.objects.get(id = instance.hospital_name.id)
            data['hospital_name'] = hospital.name
            data['hospital_id'] = hospital.id
            address = hospital.address
            location = hospital.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
            
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data.pop("location", None)
        else:
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

