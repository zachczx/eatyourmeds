from django.shortcuts import render
#from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60 * 15)
def home(request):
    return render(request, 'aboutme/home.html')

def retro(request):
    return render(request, 'aboutme/retro_home.html')