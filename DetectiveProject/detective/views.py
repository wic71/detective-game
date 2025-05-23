from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Player
from .forms import FirstDayForm
import bcrypt  # or another library if you prefer
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import get_avatar_choices
from django.contrib.auth.decorators import login_required

@login_required
def detective_office_view(request):
    player = Player.objects.get(fk_account=request.user)
    return render(request, 'detective_office.html', {
        'player': player,
    })


def home(request):
    """
    Startvyn som hälsar användaren välkommen till spelet. 
    Om användaren inte är inloggad visas länkar för registrering och inloggning.
    """
    request.session['just_signed_up'] = False
    return render(request, 'home.html')

@login_required
def first_day_view(request):
    # Försök att hämta den befintliga Player-profilen för den inloggade användaren
    try:
        player = Player.objects.get(fk_account=request.user)
    except Player.DoesNotExist:
        # Om den inte finns, skapa en ny instans kopplad till användarkontot
        player = Player(fk_account=request.user)
    
    if request.method == 'POST':
        form = FirstDayForm(request.POST, instance=player)
        if form.is_valid():
            # Uppdatera Player-profilen
            player = form.save(commit=False)
            # Du kan även uppdatera LastLoginDate eller andra fält om du önskar
            player.last_login_date = timezone.now()
            player.save()
            messages.success(request, "Dina uppgifter har sparats. Välkommen till ditt nya jobb!")
            # Omdirigera till din profilsida, eller var du vill ta användaren efter första dagen
            return redirect("profile")
    else:
        form = FirstDayForm(instance=player)
    
    return render(request, "first_day.html", {"form": form})

@login_required
def first_day_view(request):
    try:
        player = Player.objects.get(fk_account=request.user)
    except Player.DoesNotExist:
        player = Player(fk_account=request.user)

    avatar_choices = get_avatar_choices()

    if request.method == 'POST':
        form = FirstDayForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save(commit=False)
            player.last_login_date = timezone.now()
            player.save()
            messages.success(request, "Dina uppgifter har sparats.")
            return redirect("detective_office")
    else:
        form = FirstDayForm(instance=player)

    return render(request, "first_day.html", {
        "form": form,
        "avatar_choices": avatar_choices,
    })