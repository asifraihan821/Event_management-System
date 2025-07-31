from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,get_user_model,logout,authenticate
from users.forms import RegisterForm,EditProfileForm,CustomPasswordChangeForm,CustomRegistrationForm,AssignedRoleForm,CreateGroupForm
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView
from django.views.generic import TemplateView,UpdateView
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from users.models import UserProfile

User = get_user_model()

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participant(user):
    return user.groups.filter(name='participant').exists()

def sign_up(request):
    if request.method =='GET':
        form = CustomRegistrationForm()
    if request.method =='POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():             
            form.save()
            messages.success(request, 'Your sign up is succeed ! you can now log in. ')

    return render(request, 'registration/register.html', {'form':form})


def LogIn(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
    return render(request, 'registration/login.html')


class LogInView(LoginView):
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('home')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['groups'] = user.groups
        context['bio'] = user.userprofile.bio
        context['profile_picture'] = user.userprofile.profile_picture
        context['phone_number'] = user.userprofile.phone_number


        return context


class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()

        return context


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        print('views', user_profile)
        context['form'] = self.form_class(instance=self.object, userprofile=user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
    

@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('log-in')
    
    return redirect('log-in')
    
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request,'admin/dashboard.html', {'users': users})


@method_decorator(user_passes_test(is_admin,login_url='no-permission'),name='dispatch')
class AdminDashboard(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.prefetch_related(Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'NO group assigned'

        context['users'] = users
        return context
     



@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class AssignRoleView(View):
    template_name = 'admin/assign_role.html'
    form_class = AssignedRoleForm

    def get(self, request, user_id):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'{user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'form': form})




@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class CreateGroupView(CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')

    def form_valid(self, form):
        response = super().form_valid(form)
        group = form.instance
        messages.success(self.request, f'Group {group.name} has been created successfully')
        return response



@login_required
@user_passes_test(is_participant)
def participant_dashboard(request):
    events = request.user.event_set.all()  # if RSVP relation is set up
    return render(request, 'participant/dashboard.html', {'events': events})



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if is_admin(user):
                return redirect('admin-dashboard')
            elif is_organizer(user):
                return redirect('organizer-dashboard')
            elif is_participant(user):
                return redirect('participant-dashboard')
            else:
                return redirect('home') 
        
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
