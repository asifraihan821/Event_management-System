from django.urls import path
from events.views import org_dashboard,total_participants,rsvp_event,event_detail, upcoming_events,past_events,user_dashboard,create_event, total_event,update_event,delete_event,event_list,participant_dashboard

urlpatterns = [
    path('org-dashboard/', org_dashboard , name='org-dashboard'),
     path('event-list/', event_list, name='event_list'),
    path('total-participants/', total_participants, name='participants'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('past-events/',past_events , name='past-events'),
    path('user-dashboard/', user_dashboard),
    path('create-event/', create_event,name='create_event'),
    path('all-events/',total_event, name='total-events'),
    path('event/<int:event_id>/', event_detail, name='event-detail'),
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp-event'),
    path('participant-dashboard/', participant_dashboard, name='participant-dashboard'),
    path('event/update/<int:event_id>/', update_event, name='update_event'),
    path('delete-event/<int:event_id>/', delete_event, name='delete_event')
]