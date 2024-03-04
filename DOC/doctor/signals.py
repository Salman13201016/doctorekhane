import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor, DoctorService, Chamber, Experience
from user.models import User

@receiver(post_save, sender=User)
def create_doctor(sender, instance, created, **kwargs):
    if created and instance.role == 'doctor':
        name = f"{instance.first_name} {instance.last_name}"
        Doctor.objects.create(user=instance,name=name)

