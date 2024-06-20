from django.db import models
from user.models import User
from doctor.models import Chamber, Doctor
from hospital.models import Hospital,Test
from user.models import GENDER_CHOICES

# Create your models here
PATIENT_TYPES = (
    ('OPD', 'Outpatient'),
    ('IPD', 'Inpatient'),
)

PAYMENT_STATUS_CHOICES = [
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
    ]

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('cancel', 'Cancelled'),
    ('done', 'Done'),
)

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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)
    class Meta:
        unique_together = ('user', 'doctor', "chamber", "date","time") 
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        return True

# Create your models here.
class TestAppointment(models.Model):
    appointment_id = models.CharField(max_length=100,null = True, blank= True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True, blank= True)
    test = models.ForeignKey(Test,on_delete=models.SET_NULL,null= True, blank= True)
    hospital = models.ForeignKey(Hospital,on_delete=models.SET_NULL, null= True, blank= True)
    date = models.DateField(null = True, blank= True)
    time = models.TimeField(null = True, blank= True)
    fee = models.IntegerField(null = True, blank = True)
    comment = models.TextField(null=True, blank= True)
    private = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)
    class Meta:
        unique_together = ('user', 'test', "hospital", "date","time") 
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        return True

class AppointmentInfo(models.Model):
    invoice_id = models.CharField(max_length=100, null = True, blank = True)
    patient_id = models.CharField(max_length=100, null = True, blank = True)
    patient_name = models.CharField(max_length=255, null = True, blank = True)
    date = models.DateField(null = True, blank = True)
    time = models.TimeField(null = True, blank = True)
    patient_age = models.PositiveIntegerField(null = True, blank = True)
    patient_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    ref_doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,max_length=255,null = True, blank = True)
    contact_no = models.CharField(max_length=20,null = True, blank = True)
    patient_type = models.CharField(max_length=3, choices=PATIENT_TYPES,null = True, blank = True)
    chamber = models.ForeignKey(Chamber,on_delete=models.SET_NULL, null= True, blank= True)
    file_upload = models.FileField(upload_to='file/',null = True, blank = True)
    district = models.CharField(max_length=100,null = True, blank = True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null = True, blank = True)
    deleted = models.BooleanField(default=False)
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        return True