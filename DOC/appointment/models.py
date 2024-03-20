from django.db import models
from user.models import User
from doctor.models import Chamber, Doctor
# Create your models here.
class DoctorAppointment(models.Model):
    appointment_id = models.CharField(max_length=100,null = True, blank= True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True, blank= True)
    doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,null= True, blank= True,limit_choices_to={'profile': False})
    chamber = models.ForeignKey(Chamber,on_delete=models.SET_NULL, null= True, blank= True)
    date = models.DateField(null = True, blank= True)
    time = models.TimeField(null = True, blank= True)
    fee = models.IntegerField(null = True, blank = True)
    comment = models.TextField(null=True, blank= True)
    patientstatus = models.CharField(max_length=50, choices=(('new', 'New Patient'), ('old', 'Old Patient')))
    
    def __str__(self):
        return str(self.user)
    class Meta:
        unique_together = ('user', 'doctor', "chamber", "date","time") 

