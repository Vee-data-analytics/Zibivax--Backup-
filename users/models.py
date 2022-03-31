
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User

from PIL import Image
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django.urls import reverse

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID_number = models.IntegerField(default=0, null=True)

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=20,
        choices=GENDER_CHOICES,
        default=GENDER_MALE)
    
    email = models.EmailField(max_length=200, unique=True,null = True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now=True) 
    name = models.CharField(max_length = 20,default = '', null = True, unique=True )
    profile_picture = ProcessedImageField(upload_to='profilepics',
                                          processors=[ResizeToFill(100, 50)],
                                          format='JPEG',
                                          options={'quality':100})
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={"username":self.username})

    def save(self):
        super().save()
