import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor, DoctorService, Chamber, Experience

@receiver(post_save, sender=Doctor)
def create_others(sender, instance, created, **kwargs):
    if created:
        # Creating Chambers
        for chamber_data in instance.chamber.all():
            Chamber.objects.create(doctor=instance, hospital=chamber_data.hospital, address=chamber_data.address)

        # Creating Experiences
        for experience_data in instance.experiences.all():
            Experience.objects.create(doctor=instance, start_date=experience_data.start_date, end_date=experience_data.end_date, designation=experience_data.designation, working_place=experience_data.working_place)

        # Creating DoctorServices
        for service_data in instance.services.all():
            DoctorService.objects.create(doctor=instance, service_name=service_data.service_name)

