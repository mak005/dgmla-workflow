from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import ConnexionForm, ChangerMDPForm
from .models import Agent


class ConnexionView(LoginView):
    template_name = "comptes/connexion.html"
    authentication_form = ConnexionForm

    def get_success_url(self):
        if self.request.user.doit_changer_mdp:
            return reverse_lazy("changer_mot_de_passe")
        return reverse_lazy("dashboard")


class ChangerMotDePasseView(PasswordChangeView):
    template_name = "comptes/changer_mot_de_passe.html"
    form_class = ChangerMDPForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        self.request.user.doit_changer_mdp = False
        self.request.user.save()
        return super().form_valid(form)


# Create your views here.
