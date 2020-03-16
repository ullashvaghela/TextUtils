from djongo import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=30,blank=True,null=True)
    state = models.CharField(max_length=30,blank=True,null=True)
    zipcode = models.PositiveIntegerField(blank=True,null=True)
    mobile_number = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return self.user.email

class BlackList(models.Model):
    token = models.CharField('token', max_length=255,unique=True)
    created_date_time = models.DateTimeField(default=timezone.now)
    updated_date_time = models.DateTimeField(default=timezone.now, editable=True)
    


