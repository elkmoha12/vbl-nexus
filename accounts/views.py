from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from boxers.models import Boxer, Club
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from boxers.models import Boxer, Club, Combat


def dashboard(request):
    context = {
        'boxers_count': Boxer.objects.count(),
        'clubs_count': Club.objects.count(),
        'events_count': 0,
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Ongeldige gebruikersnaam of wachtwoord."
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def toegangen(request):
    error = None
    success = None
    
    if request.method == 'POST':
        voornaam = request.POST.get('voornaam')
        achternaam = request.POST.get('achternaam')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            error = f"Gebruikersnaam '{username}' bestaat al."
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=voornaam,
                last_name=achternaam
            )
            UserProfile.objects.create(user=user, role=role)
            success = f"Gebruiker '{username}' aangemaakt als {role}."
    
    users = UserProfile.objects.select_related('user').all()
    return render(request, 'toegangen.html', {
        'users': users,
        'error': error,
        'success': success
    })

@login_required
def palmares(request):
    error = None
    success = None
    boxers = Boxer.objects.all()

    if request.method == 'POST':
        boxer_id = request.POST.get('boxer')
        tegenstander = request.POST.get('tegenstander')
        datum = request.POST.get('datum')
        evenement = request.POST.get('evenement')
        resultaat = request.POST.get('resultaat')

        boxer = Boxer.objects.get(id=boxer_id)
        Combat.objects.create(
            boxer=boxer,
            tegenstander=tegenstander,
            datum=datum,
            evenement=evenement,
            resultaat=resultaat
        )

        # Update palmares
        if resultaat == 'overwinning':
            boxer.overwinningen += 1
        elif resultaat == 'verlies':
            boxer.verlies += 1
        elif resultaat == 'gelijkspel':
            boxer.gelijkspel += 1
        boxer.save()

        success = f"Resultaat opgeslagen voor {boxer}."

    combats = Combat.objects.select_related('boxer').order_by('-datum')[:20]
    return render(request, 'palmares.html', {
        'boxers': boxers,
        'combats': combats,
        'error': error,
        'success': success
    })

@login_required
def rusttijd(request):
    error = None
    success = None
    boxers = Boxer.objects.all()

    if request.method == 'POST':
        boxer_id = request.POST.get('boxer')
        rusttijd_tot = request.POST.get('rusttijd_tot')
        
        boxer = Boxer.objects.get(id=boxer_id)
        boxer.rusttijd_tot = rusttijd_tot
        boxer.save()
        success = f"Rusttijd opgeslagen voor {boxer} tot {rusttijd_tot}."

    boxers_in_rust = Boxer.objects.filter(rusttijd_tot__isnull=False).order_by('rusttijd_tot')
    return render(request, 'rusttijd.html', {
        'boxers': boxers,
        'boxers_in_rust': boxers_in_rust,
        'error': error,
        'success': success
    })