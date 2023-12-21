from django.db import models


# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.name}"
    
class District(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.name}"
    
class State(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.name}"

