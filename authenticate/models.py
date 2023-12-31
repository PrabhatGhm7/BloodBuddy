from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#created a class Userprofile with instance of User to connect the left info of user in myuser.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname =models.CharField(max_length=255, blank =False)
    age = models.IntegerField(blank=False)
    address = models.CharField(max_length=255,  blank=False)
    bloodgroup = models.CharField(max_length=5, blank =False)
    gender = models.CharField(max_length=7 , blank =False)
    
    def __str__(self):
        return self.fullname
    
    

