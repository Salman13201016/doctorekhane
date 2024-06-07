import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hospital,Ambulance
from user.models import User

@receiver(post_save, sender=User)
def create_hospital(sender, instance, created, **kwargs):
    if created and instance.role == 'hospital':
        name = f"{instance.first_name}"
        Hospital.objects.create(user=instance,email=instance.email,name=name,profile=True)

@receiver(post_save, sender=User)
def create_ambulance(sender, instance, created, **kwargs):
    if created and instance.role == 'ambulance':
        name = f"{instance.first_name}"
        Ambulance.objects.create(user=instance,name=name,profile=True)