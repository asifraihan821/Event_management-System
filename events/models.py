from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
'''● Event:
○ Fields: name, description, date, time, location, category (ForeignKey)
● Participant:
○ Fields: name, email, and a ManyToMany relationship with Event.
● Category:
○ Fields: name and description.'''




class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    asset = models.ImageField(upload_to='event_asset', blank=True,null=True, default='event_asset/defaultpng.png')
    attendees = models.ManyToManyField(User, related_name="rsvped_events", blank=True)

    def __str__(self):
        return self.name
    
    def get_asset_url(self):
        if self.asset and hasattr(self.asset, 'url'):
            return self.asset.url
        return settings.MEDIA_URL + 'event_asset/default.png'



class Participants(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    event = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name
    

# @receiver(post_save,sender=Event )
# def notify_event_creation(sender,instance,created,**kwargs):
#     if created:
