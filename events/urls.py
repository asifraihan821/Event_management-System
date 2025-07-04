from django.urls import path
from events.views import org_dashboard,total_participants, upcoming_events,past_events,user_dashboard,test

urlpatterns = [
    path('org-dashboard/', org_dashboard),
    path('total-participants/', total_participants),
    path('upcoming-events/', upcoming_events),
    path('past-events/',past_events),
    path('user-dashboard/', user_dashboard),
    path('test/', test)
]
