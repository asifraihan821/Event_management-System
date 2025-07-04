from django.urls import path
from events.views import main_dashboard,total_participants, upcoming_events,past_events

urlpatterns = [
    path('main-dashboard/', main_dashboard),
    path('total-participants/', total_participants),
    path('upcoming-events/', upcoming_events),
    path('past-events/',past_events)
]
