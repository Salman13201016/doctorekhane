import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hospital
from user.models import User

@receiver(post_save, sender=User)
def create_hospital(sender, instance, created, **kwargs):
    if created and instance.role == 'hospital':
        name = f"{instance.first_name} {instance.last_name}"
        Hospital.objects.create(user=instance,name=name,profile=True)

