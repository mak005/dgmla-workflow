from django.urls import path
from .views import ConnexionView, ChangerMotDePasseView, deconnexion
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('changer-mot-de-passe/', ChangerMotDePasseView.as_view(), name='changer_mot_de_passe'),
]