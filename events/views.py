from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('welcome to home')

def contact(request):
    return HttpResponse('<h1>welcome to contact</h2>')

def show_task(request):
    return HttpResponse('<h1>welcome to our showtask page</h2>')