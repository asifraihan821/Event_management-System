from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name ='userprofile',primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_image',blank=True,null=True)
    bio = models.TextField()
    phone_number = models.CharField(blank=True,null=True)

    def __str__(self):
        return self.user.username


