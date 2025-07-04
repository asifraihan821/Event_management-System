from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main_dashboard(request):
    return render(request, 'org_dashboard.html')

def total_participants(request):
    return render(request, 'total_participants.html')

def upcoming_events(request):
    return render(request, 'upcoming_events.html')

def past_events(request):
    return render(request, 'user_past_events.html')