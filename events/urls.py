from django.urls import path
from events.views import OrgDashboardView,total_participants,rsvp_event, upcoming_events,past_events,UserDashboardView, total_event,update_event,delete_event,event_list,participant_dashboard,EventDetailView,CreateEventView,dashboard

urlpatterns = [
    path('org-dashboard/', OrgDashboardView.as_view() , name='org-dashboard'),
     path('event-list/', event_list, name='event_list'),
    path('total-participants/', total_participants, name='participants'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('past-events/',past_events , name='past-events'),
    path('user-dashboard/', UserDashboardView.as_view(),name='user-dashboard'),
    path('create-event/', CreateEventView.as_view(),name='create-event'),
    path('all-events/',total_event, name='all-events'),
    path('event/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp-event'),
    path('participant-dashboard/', participant_dashboard, name='participant-dashboard'),
    path('event/update/<int:event_id>/', update_event, name='update_event'),
    path('delete-event/<int:event_id>/', delete_event, name='delete_event'),
    path('dashboard/', dashboard, name='dashboard')
]