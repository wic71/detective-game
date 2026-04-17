from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Player
from .forms import FirstDayForm
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
