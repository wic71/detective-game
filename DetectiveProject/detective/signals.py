# detective/signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def set_signup_flag(request, user, **kwargs):
    # Sätt en flagga i sessionen för nyregistrerade användare
    print("DEBUG 1a: user_signed_up signal triggered")
    request.session['just_signed_up'] = True