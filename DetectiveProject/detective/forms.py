# detective/forms.py
from django import forms
from .models import Player
import os
from django.conf import settings


def get_avatar_choices():
    """
    Hämtar en lista med avatars från katalogen detective/images/avatars,
    och returnerar en lista med tuples: (avatar_url, filename).
    Förutsätter att dina statiska filer serveras från /static/
    och att avatarmappen ligger under detective/static/detective/images/avatars/.
    """
    # Anta att dina statiska filer ligger i BASE_DIR/detective/static/
    avatar_dir = os.path.join(settings.BASE_DIR, "detective", "static", "detective", "images", "avatars")
    choices = []
    try:
        for file in os.listdir(avatar_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Skapa URL:en, här antas att avatars ligger på /static/detective/images/avatars/<file>
                url = f"/static/detective/images/avatars/{file}"
                choices.append((url, file))
    except Exception as e:
        # Om katalogen inte finns eller annat, returnera tom lista
        print("Error loading avatars:", e)
    return choices

class FirstDayForm(forms.ModelForm):
    avatar_url = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,  # Byt ut till radio‑knappar
        label="Välj Avatar",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar_url"].choices = get_avatar_choices()

    class Meta:
        model = Player
        fields = ["in_game_first_name", "in_game_last_name", "avatar_url"]
        labels = {
            "in_game_first_name": "Förnamn",
            "in_game_last_name": "Efternamn",
        }
