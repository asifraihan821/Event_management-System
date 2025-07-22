from django.urls import path
from users.views import sign_up, LogIn,custom_login, signout,admin_dashboard,assign_role,create_group


urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    path('log-in/', LogIn, name='log-in'),
    path('log-out/', signout, name='log-out'),
    path('admin/dashboard/', admin_dashboard, name= 'admin-dashboard'),
    path('admin/<int:user_id>/assign_role/', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name='create-group'),
    path('login/', custom_login, name='login'),
]
