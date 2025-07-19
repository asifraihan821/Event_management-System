from django.urls import path
from users.views import sign_up, LogIn, signout


urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    path('log-in/', LogIn, name='log-in'),
    path('log-out/', signout, name='log-out')
]
