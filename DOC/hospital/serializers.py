from rest_framework import serializers
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from user.models import User

from .models import Hospital,Ambulance,Test,TestCatagory,HospitalService
from app.models import Specialist
from doctor.models import Chamber
from django.db.models import Q




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
        catagory_name_bn = catagory_data.get('name_bn')
        catagory_instance = TestCatagory.objects.filter(Q(name=catagory_name)|Q(name_bn = catagory_name_bn)).first()
        if self.instance:
            if Test.objects.filter(Q(test_name__iexact=attrs.get('test_name'))|Q(test_name_bn__iexact=attrs.get('test_name_bn')), catagory=catagory_instance).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Test with this catagory already exists.'})
        else:
            if Test.objects.filter(Q(test_name__iexact=attrs.get('test_name'))|Q(test_name_bn__iexact=attrs.get('test_name_bn')), catagory=catagory_instance).exists():
                raise serializers.ValidationError({'message': 'Test with this catagory already exists.'})
        return attrs

    
    def create(self, validated_data):
        catagory_data = validated_data.pop('catagory')
        catagory_name = catagory_data.get('name')
        catagory_name_bn = catagory_data.get('name_bn')
        catagory_instance, _ = TestCatagory.objects.get_or_create(name=catagory_name,name_bn=catagory_name_bn)
        
        validated_data['catagory'] = catagory_instance
        return Test.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        catagory_data = validated_data.pop('catagory', None)  # Get catagory data or None if not present
        if catagory_data:
            catagory_id = catagory_data.get('id')
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
            'name': catagory_instance.name,
            'name_bn': catagory_instance.name_bn
        }
        
        return data


class HospitalServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = HospitalService
        fields = "__all__"
        extra_kwargs = {
            'id' : {'read_only': False},
        }

    # def validate(self, attrs):
    #     if self.instance:
    #         if HospitalService.objects.filter(service_name__iexact=attrs.get('service_name'), hospital=attrs.get('hospital')).exclude(id=self.instance.id).exists():
    #             raise serializers.ValidationError({"message": 'Hospital With Same Service already exists'})
    #     elif HospitalService.objects.filter(service_name__iexact=attrs.get('service_name'), hospital=attrs.get('hospital')).exists():
    #         raise serializers.ValidationError({"message": 'Hospital With Same Service already exists'})
    #     return attrs

class HospitalProfileSerializer(serializers.ModelSerializer):
    hospital_image = Base64ImageField(required=False,allow_null=True)
    services = HospitalServiceSerializer(required = False, allow_null = True, many = True)

    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'name_bn': {'required': True},
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
                    specialists.append({"id": specialist.id,"name": specialist.specialist_name,"name_bn": specialist.specialist_name_bn})
            data['specialist'] = specialists


            test_ids = data.pop('tests', [])
            tests = []
            for test_id in test_ids:
                test = Test.objects.filter(id=test_id).first()
                if test:
                    tests.append({"id": test.id,"name": test.test_name, "name_bn": test.test_name_bn})  # Replace 'specialist_name' with the correct attribute name
            data['test'] = tests
            data['doctor_count'] = Chamber.objects.filter(hospital=instance).count()
            return data

class HospitalProfileManagementSerializer(serializers.ModelSerializer):
    hospital = HospitalProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'is_superuser', 'hospital']
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
        services_data = hospital_data.pop('services', None)

        if 'specialists' in hospital_data:
            instance.hospital.specialists.set(hospital_data.pop('specialists'))

        if 'tests' in hospital_data:
            instance.hospital.tests.set(hospital_data.pop('tests'))


        # Update hospital fields
        for attr, value in hospital_data.items():
            setattr(instance.hospital, attr, value)
        instance.hospital.save()

        if services_data:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    service_instance = HospitalService.objects.filter(id=service_id).first()
                    if service_instance:
                        # Update service instance attributes
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    service_instance, _ = HospitalService.objects.get_or_create(service_name=service_data.get("service_name"))
                    instance.services.add(service_instance)
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
    services = HospitalServiceSerializer(required = False, allow_null = True, many = True)

    class Meta:
        model = Hospital
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'name_bn': {'required': True},
            'hospital_image': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'slug':{'read_only':True},
            'slug_bn':{'read_only':True},
            'website': {'required': False},
        }
    def validate(self, attrs):
        if self.instance:
            if Hospital.objects.filter(Q(name__iexact=attrs.get('name'))|Q(name_bn__iexact=attrs.get('name_bn')),Q(address=attrs.get('address'))|Q(address_bn=attrs.get('address_bn')),profile=False).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'message': 'Hospital at this address already exists.'})
        else:
            if Hospital.objects.filter(Q(name__iexact=attrs.get('name'))|Q(name_bn__iexact=attrs.get('name_bn')),Q(address=attrs.get('address'))|Q(address_bn=attrs.get('address_bn')),profile=False).exists():
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
        gethospital_serviceInfo = validated_data.pop('services', [])

        tests_data = validated_data.pop('tests', [])

        hospital = Hospital.objects.create(**validated_data)
        hospital.specialists.set(specialists_data)
        for service_data in gethospital_serviceInfo:
            service_instance, _ = HospitalService.objects.get_or_create(service_name=service_data.get("service_name"),service_name_bn=service_data.get("service_name_bn"))
            hospital.services.add(service_instance)
        hospital.tests.set(tests_data)

        return hospital

    def update(self, instance, validated_data):
        if 'specialists' in validated_data:
            instance.specialists.set(validated_data.pop('specialists'))
        services_data = validated_data.pop('services', None)

        if 'tests' in validated_data:
            instance.tests.set(validated_data.pop('tests'))

        # Update hospital fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update related services
        if services_data:
            for service_data in services_data:
                service_id = service_data.get('id')
                if service_id:
                    service_instance = HospitalService.objects.filter(id=service_id).first()
                    if service_instance:
                        # Update service instance attributes
                        for attr, value in service_data.items():
                            setattr(service_instance, attr, value)
                        service_instance.save()
                else:
                    service_instance, _ = HospitalService.objects.get_or_create(service_name=service_data.get("service_name"),service_name_bn=service_data.get("service_name_bn"))
                    instance.services.add(service_instance)
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
                specialists.append({"id": specialist.id,"name": specialist.specialist_name,"name_bn": specialist.specialist_name_bn})
        data['specialist'] = specialists

        test_ids = data.pop('tests', [])
        tests = []
        for test_id in test_ids:
            test = Test.objects.filter(id=test_id).first()
            if test:
                tests.append({"id": test.id,"name": test.test_name,"name_bn": test.test_name_bn})  # Replace 'specialist_name' with the correct attribute name
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
            'slug_bn':{'read_only':True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.hospital:
            hospital = Hospital.objects.get(id = instance.hospital_name.id)
            data['hospital_id'] = hospital.id
            data['hospital_name'] = hospital.name
            data['hospital_name_bn'] = hospital.name_bn
            address = hospital.address
            address_bn = hospital.address_bn
            location = hospital.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
            
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data["Address_BN"] = ", ".join(filter(None, [address_bn, union_name, upazila_name, district_name, division_name]))
            data.pop("location", None)
        else:
            address = instance.address
            address_bn = instance.address_bn
            location = instance.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
        
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data["Address_BN"] = ", ".join(filter(None, [address_bn, union_name, upazila_name, district_name, division_name]))
            data.pop("location", None)
        return data
    
class AmbulanceManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = "__all__"
        extra_kwargs = {
            'hospital_name': {'required': False},
            'hospital_name_bn': {'required': False},
            'slug':{'read_only':True},
            'slug_bn':{'read_only':True},
        }

    def validate(self, data):
        if data.get('hospital') and not data.get('hospital_name') and not data.get('hospital_name_bn'):
            raise serializers.ValidationError({"message":"Hospital name cannot be empty if hospital is True."})
        return data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.hospital :# Including division, district, and upazila information in the representation
            hospital = Hospital.objects.get(id = instance.hospital_name.id)
            data['hospital_name'] = hospital.name
            data['hospital_name_bn'] = hospital.name_bn
            data['hospital_id'] = hospital.id
            address = hospital.address
            address_bn = hospital.address_bn
            location = hospital.location

            union_name = location.union_name if location else ""
            upazila_name = location.upazila.upazila_name if location and location.upazila else ""
            district_name = location.upazila.district.district_name if location and location.upazila and location.upazila.district else ""
            division_name = location.upazila.district.division.division_name if location and location.upazila and location.upazila.district and location.upazila.district.division else ""
            
            data["Address"] = ", ".join(filter(None, [address, union_name, upazila_name, district_name, division_name]))
            data["Address_BN"] = ", ".join(filter(None, [address_bn, union_name, upazila_name, district_name, division_name]))
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

