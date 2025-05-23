from allauth.account.adapter import DefaultAccountAdapter

class DetectiveAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        print("DEBUG 2a: in get_login_redirect_url, session:", request.session)

        if request.session.get('just_signed_up', False):
            print("Debug 2c: ",request.session['just_signed_up'])
            del request.session['just_signed_up']
            return '/first-day/'
        return '/detective_office/' #super().get_login_redirect_url(request)
    

