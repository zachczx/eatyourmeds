from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home(request):
    return render(request, 'aboutme/home.html')

def retro(request):
    return render(request, 'aboutme/retro_home.html')