from django.shortcuts import render
from .models import Boxer, Club

def boxers_list(request):
    boxers = Boxer.objects.all()
    return render(request, 'boxers.html', {'boxers': boxers})

def clubs_list(request):
    clubs = Club.objects.all()
    return render(request, 'clubs.html', {'clubs': clubs})
