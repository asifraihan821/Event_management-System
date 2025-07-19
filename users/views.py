from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegistrationForm

# Create your views here.
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


def signout(request):
    
    if request.method == 'POST':
        logout(request)
        return redirect('log-in')
    