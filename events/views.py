from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def org_dashboard(request):
    return render(request, 'dashboard/org_dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')

def total_participants(request):
    return render(request, 'total_participants.html')

def upcoming_events(request):
    return render(request, 'upcoming_events.html')

def past_events(request):
    return render(request, 'user_past_events.html')