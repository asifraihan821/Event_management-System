from django.urls import path
from events.views import show_task

urlpatterns = [
    path('show-task/', show_task)
]
