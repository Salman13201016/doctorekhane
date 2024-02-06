from rest_framework import serializers
from .models import Blog
from drf_extra_fields.fields import Base64ImageField

class BlogManagementSerializer(serializers.ModelSerializer):
    img = Base64ImageField(required=True)
    class Meta:
        model=Blog
        fields = "__all__"
        extra_kwargs = {
            'img' : {'required':False},
            'author':{'read_only':True},
            'slug':{'required':False},
        }

    def validate(self, value):
        """
        Validate that the name of the community is unique.
        """
        if Blog.objects.filter(title=value).exists():
            raise serializers.ValidationError("A Blog with this title already exists.")
        return value
    
    def create(self, validated_data):
        """
        Override the create method to set the slug to be the same as the title.
        """
        validated_data['author'] = self.context['request'].user
        if validated_data['author'].profile.role == "admin" or validated_data['author'].profile.role == "superadmin":
            validated_data['published'] = True
        validated_data['slug'] = validated_data['title'].lower().replace(" ", "-").replace(",", "").replace("&","and")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Override the update method to update the instance and set the slug based on the title.
        """
        for field in self.Meta.model._meta.fields:
            field_name = field.name
            if field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])

        # Set the slug based on the updated title
        instance.slug = instance.title.lower().replace(" ", "-").replace(",", "").replace("&","and")

        instance.save()
        return instance
    
    def to_representation(self , instance):
        data = super().to_representation(instance)
        data["author name"] = f'{instance.author.first_name} {instance.author.last_name}'
        
        return data