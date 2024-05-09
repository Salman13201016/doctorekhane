# signals.py
import base64
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'general':
        Profile.objects.create(user=instance)

