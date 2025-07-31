from django.shortcuts import render,redirect,get_object_or_404
from events.models import Category,Event,Participants
from datetime import date
from django.db.models import Q, Min, Max, Count
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from users.views import is_admin
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views import View



# Create your views here.
def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participants(user):
    return user.groups.filter(name='participants').exists()

def has_required_role(user):
    return is_participants(user) or is_organizer(user) or is_admin(user)


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('org-dashboard')
    elif is_participants(request.user):
        return redirect('participant-dashboard')
    else:
        return redirect('user-dashboard')


@method_decorator(user_passes_test(has_required_role, login_url='no-permission'), name='dispatch')
class OrgDashboardView(TemplateView):
    template_name = 'dashboard/org_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        type = request.GET.get('type', 'all')
        today = date.today()

        # Count values
        context['events'] = Event.objects.count()
        context['todays_events'] = Event.objects.filter(date=today)
        context['upcoming_events'] = Event.objects.filter(date__gt=today).count()
        context['past_events'] = Event.objects.filter(date__lt=today).count()
        context['total_participants'] = Participants.objects.count()

        # Filtered event list
        if type == 'totalEvents':
            context['all_events'] = Event.objects.all()
        elif type == 'upcoming':
            context['all_events'] = Event.objects.filter(date__gt=today)
        elif type == 'past':
            context['all_events'] = Event.objects.filter(date__lt=today)
        elif type == 'participants':
            context['all_events'] = []  # Or provide participant data if needed
        elif type == 'all':
            context['all_events'] = Event.objects.prefetch_related('participants').annotate(partcpnts=Count('participants'))

        return context



@method_decorator(login_required, name='dispatch')
class UserDashboardView(TemplateView):
    template_name = 'dashboard/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        context['events'] = Event.objects.select_related().count()
        context['all_events'] = Event.objects.prefetch_related('participants').annotate(
            partcpnts=Count('participants')
        )
        context['todays_events'] = Event.objects.filter(date=today)
        context['upcoming_events'] = Event.objects.filter(date__gt=today).count()
        context['past_events'] = Event.objects.filter(date__lt=today).count()
        context['total_participants'] = Participants.objects.count()

        return context



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




@method_decorator(user_passes_test(is_admin,login_url='no-permission'), name = 'dispatch')
class CreateEventView(View):

    def get(self,request,*args,**kwargs):
        return render(request, 'create_event.html')

    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        category = request.POST.get('category')
        category_description = request.POST.get('category_description')
        asset = request.FILES.get('asset')

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
                category=category,
                asset = asset
            )
            messages.success(request, "Event added successfully")
            return redirect('create-event')

        messages.error(request, "All fields are required.")
        return render(request, 'create_event.html')


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



class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    pk_url_kwarg = 'event_id'
    context_object_name = 'event'

