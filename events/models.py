from django.db import models

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
    location = models.CharField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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