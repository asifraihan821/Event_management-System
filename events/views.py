from django.shortcuts import render,redirect,get_object_or_404
from events.models import Category,Event,Participants
from datetime import date
from django.db.models import Q, Min, Max, Count
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from users.views import is_admin
from django.core.mail import send_mail

# Create your views here.
def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participants(user):
    return user.groups.filter(name='participants').exists()

def has_required_role(user):
    return is_participants(user) or is_organizer(user) or is_admin(user)


@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def org_dashboard(request):
    type = request.GET.get('type', 'all')
    today = date.today()

    # Count values
    total_events_count = Event.objects.count()
    total_participants_count = Participants.objects.count()
    upcoming_events_count = Event.objects.filter(date__gt=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    all_events = Event.objects.prefetch_related('participants').annotate(partcpnts=Count('participants'))
    todays_events = Event.objects.filter(date=today)


    if type == 'totalEvents':
        all_events = Event.objects.all()
    elif type == 'upcoming':
        all_events = Event.objects.filter(date__gt=today)
    elif type == 'past':
        all_events = Event.objects.filter(date__lt=today)
    elif type == 'participants':
        # You could return participant list here if needed
        pass
    elif type == 'all':
        all_events = Event.objects.prefetch_related('participants').annotate(partcpnts=Count('participants'))

    return render(request, 'dashboard/org_dashboard.html', {
        'events': total_events_count,
        'todays_events': todays_events,
        'upcoming_events': upcoming_events_count,
        'past_events': past_events_count,
        'total_participants': total_participants_count,
        'all_events': all_events
    })



@login_required
def user_dashboard(request):
    today = date.today()
    events = Event.objects.select_related().count()
    all_events = Event.objects.prefetch_related('participants').annotate(partcpnts = Count('participants'))
    todays_events = Event.objects.filter(date = today)
    upcoming_events = Event.objects.filter(date__gt = today).count()
    past_events = Event.objects.filter(date__lt = today).count()
    total_participants = Participants.objects.count()

    return render(request, 'dashboard/user_dashboard.html',{'events':events, 'todays_events':todays_events, 'upcoming_events':upcoming_events, 'past_events':past_events, 'total_participants':total_participants,'all_events':all_events})

@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def total_participants(request):
    participants = Event.objects.annotate(partcpnts = Count('participants'))
    return render(request, 'total_participants.html', {'participants':participants})

@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def upcoming_events(request):
    today = date.today()
    events = Event.objects.prefetch_related('participants').annotate(partcpnts = Count('participants')).filter(date__gt = today)    
    return render(request, 'upcoming_events.html',{'events':events})


@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def past_events(request):
    today = date.today()
    events = Event.objects.prefetch_related('participants').annotate(partcpnts = Count('participants')).filter(date__lt = today)    
    return render(request, 'user_past_events.html', {'events':events})

@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def create_event(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        category = request.POST.get('category')
        category_description = request.POST.get('category_description')

        if name and description and date and location and category and category_description:
            category, created = Category.objects.get_or_create(name=category)
            if created:
                category.description = category_description
                category.save()

            Event.objects.create(
                name=name,
                description=description,
                date=date,
                location=location,
                category=category
            )
            messages.success(request, "Event added successfully")
            return redirect('org-dashboard')
        
    return redirect('org-dashboard')

from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event, Category
from django.contrib import messages

@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        category_name = request.POST.get('category')
        location = request.POST.get('location')
        date = request.POST.get('date')
        description = request.POST.get('description')
        category_description = request.POST.get('category_description')
        
        if name and category_name and location and date and description and category_description:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                category.description = category_description
                category.save()
            
            # Update the event fields
            event.name = name
            event.category = category
            event.location = location
            event.date = date
            event.description = description
            event.save()
            
            messages.success(request, "Event updated successfully.")
            return redirect('org-dashboard') 
            
        else:
            messages.error(request, "Please fill in all fields.")
    
    return render(request, 'update_event.html', {'event': event})

@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully")
    return redirect('org-dashboard')


@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def total_event(request):
    events = Event.objects.prefetch_related('participants').annotate(partcpnts = Count('participants'))
    return render(request, 'user_AllEvents.html', {'events':events})
     
@login_required
@user_passes_test(has_required_role,login_url='no-permission')
def event_list(request):
    return render(request, 'events/event_list.html')



@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user not in event.attendees.all():
        event.attendees.add(user)
        messages.success(request, "RSVP successful. Confirmation email sent.")

    return redirect('event-detail', event_id=event.id)


@login_required
def participant_dashboard(request):
    events = request.user.rsvped_events.all()
    return render(request, 'dashboard/participant_dashboard.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})