from django.contrib import admin
from events.models import Event,Participants,Category

# Register your models here.

admin.site.register(Event)
admin.site.register(Participants)
admin.site.register(Category)
