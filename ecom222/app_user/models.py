from djongo import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
import datetime

now = datetime.datetime.now()

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100,blank=True)
    state =  models.CharField(max_length=100,blank=True)
    zipcode= models.IntegerField(blank=True)
    contact_number= models.IntegerField(blank=True)
   
    USERNAME_FIELD = 'username'
   
    def __str__(self):
        return self.username

class BlackList(models.Model):
    created_date_time = models.DateTimeField(default=timezone.now)
    updated_date_time = models.DateTimeField(default=timezone.now, editable=True)
    token = models.CharField('token', max_length=255,unique=True)

class UserVerification(models.Model):
    USER_VERIFICATION_TYPES = (
        ('VERIFY', 'email_verification'),
        ('FORGOT', 'forgot_password')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=6, default="")
    verification_type = models.CharField(max_length=15, choices=USER_VERIFICATION_TYPES, default=USER_VERIFICATION_TYPES[0][0])
    created_date_time = models.DateTimeField(auto_now=True, editable=True)
    
    def __str__(self):
        return str(self.created_date_time)
