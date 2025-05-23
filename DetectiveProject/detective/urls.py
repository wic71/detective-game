
# DetectiveProject/detective/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Om du vill använda din egen signup-vy istället för allauths:
    #path('signup/', views.signup_view, name='signup'),
    path('detective_office/', views.detective_office_view, name='detective_office'),
    path('first-day/', views.first_day_view, name='first_day'),
    # Lägg till andra sidor specifika för din applikation...
]
