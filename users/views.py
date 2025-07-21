from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegistrationForm,AssignedRoleForm,CreateGroupForm
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


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