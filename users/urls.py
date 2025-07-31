from django.urls import path
from users.views import sign_up, signout,LogInView,AssignRoleView,AdminDashboard,CreateGroupView,CustomPasswordResetView,ProfileView,EditProfileView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView


urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    path('log-in/', LogInView.as_view(), name='log-in'),
    path('log-out/', LogoutView.as_view(next_page='/'), name='log-out'),
    path('admin/dashboard/', AdminDashboard.as_view(), name= 'admin-dashboard'),
    path('admin/<int:user_id>/assign_role/', AssignRoleView.as_view(), name="assign-role"),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/',PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'),name='password_change_done'),
    path('password_reset/',CustomPasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',PasswordResetDoneView.as_view(),name='password_reset_done'), 
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_confirm/',PasswordResetCompleteView.as_view()),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile')
]
