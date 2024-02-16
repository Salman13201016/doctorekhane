from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Specialist, Doctor, Chamber , DoctorService , Experience

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

class ChamberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamber
        fields = "__all__"

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

class DoctorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorService
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False,allow_null=True)
    chamber = ChamberSerializer(required = False, allow_null = True, many = True)
    experience_details = ExperienceSerializer(required = False, allow_null = True, many = True)
    doctor_service = DoctorServiceSerializer(required = False, allow_null = True, many = True)
    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
             'license_no' : { 'required': True }, 
             'specialists' : { 'required': True }, 
             'qualification' : { 'required': True }, 
             'slug': {'read_only': True},
        }
        def validate(self , attrs):
            if self.instance:
                if  Doctor.objects.filter(license_no__iexact=attrs.get('license_no')).exclude(id=self.instance.id).exists():
                            raise serializers.ValidationError({"message": 'License No already exists'})
            elif Doctor.objects.filter(license_no__iexact=attrs.get('license_no')).exists():
                raise serializers.ValidationError({"message": 'License No already exists.'})
            return attrs
        
    def create(self, validated_data):
        getchamberInfo = validated_data.pop('chamber', [])
        getexperience_detailsInfo = validated_data.pop('experience_details', [])
        getdoctor_serviceInfo = validated_data.pop('doctor_service', [])
        specialists_data = validated_data.pop('specialists', [])

        doctor = Doctor.objects.create(**validated_data)
        doctor.specialists.set(specialists_data)

        for chamber_data in getchamberInfo:
            Chamber.objects.create(doctor=doctor, **chamber_data)

        for experience_data in getexperience_detailsInfo:
            Experience.objects.create(doctor=doctor, **experience_data)

        for service_data in getdoctor_serviceInfo:
            DoctorService.objects.create(doctor=doctor, **service_data)

        return doctor

    def update(self, instance, validated_data):
        if 'chember' in validated_data:
            for item, value in validated_data.pop('chember').items():
                setattr(instance.chember, item, value)
            
            instance.chamber.save()
        if 'experience' in validated_data:
            for item, value in validated_data.pop('experience').items():
                setattr(instance.experience, item, value)
            
            instance.experience.save()
        if 'doctor_service' in validated_data:
            for item, value in validated_data.pop('doctor_service').items():
                setattr(instance.doctor_service, item, value)
            
            instance.doctor_service.save()
        # update user
        for item, value in validated_data.items():
            setattr(instance, item, value)
        instance.save()
        
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'profile_image' in data and data['profile_image']:
            data['profile_image'] = instance.profile_image.url

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
        specialist_names = []
        for specialist_id in specialist_ids:
            specialist = Specialist.objects.filter(id=specialist_id).first()
            if specialist:
                specialist_names.append(specialist.specialist_name)  # Replace 'specialist_name' with the correct attribute name
        data['specialist'] = specialist_names
        return data
