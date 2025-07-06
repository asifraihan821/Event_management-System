from django.urls import path
from events.views import org_dashboard,total_participants, upcoming_events,past_events,user_dashboard,create_event, total_event,update_event,delete_event

urlpatterns = [
    path('org-dashboard/', org_dashboard , name='org-dashboard'),
    path('total-participants/', total_participants, name='participants'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('past-events/',past_events , name='past-events'),
    path('user-dashboard/', user_dashboard),
    path('create-event/', create_event,name='create_event'),
    path('all-events/',total_event, name='total-events'),
    path('event/update/<int:event_id>/', update_event, name='update_event'),
    path('delete-event/<int:event_id>/', delete_event, name='delete_event')
]
