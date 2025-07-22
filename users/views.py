from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegistrationForm,AssignedRoleForm,CreateGroupForm
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from django.contrib.auth.forms import AuthenticationForm

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



@login_required
def signout(request):

    if request.method == 'POST':
        logout(request)
        return redirect('log-in')
    

    
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request,'admin/dashboard.html', {'users': users})



@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
   
    form = AssignedRoleForm()
    
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f'{user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')
        

    return render(request, 'admin/assign_role.html', {'form':form})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('create-group')
        
    return render(request, 'admin/create_group.html', {'form':form})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):
    return render(request, 'organizer/dashboard.html')

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
