from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import ConnexionForm, ChangerMDPForm
from .models import Agent
from datetime import datetime, timezone
from django.contrib.auth import logout


class ConnexionView(LoginView):
    template_name = "comptes/connexion.html"
    authentication_form = ConnexionForm

    # Redirection vers la page de changement de mot de passe
    def get_success_url(self):
        if self.request.user.doit_changer_mdp:
            return reverse_lazy("changer_mot_de_passe")
        return reverse_lazy("dashboard")

    # Recuperation de l'heure de deblocage du compte
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matricule = self.request.POST.get("username")
        if matricule:
            agent = Agent.objects.filter(matricule=matricule).first()
            if (
                agent
                and agent.bloque_jusqu_a
                and agent.bloque_jusqu_a > datetime.now(timezone.utc)
            ):
                context["bloque_jusqu_a_timestamp"] = str(agent.bloque_jusqu_a.timestamp())
        return context


class ChangerMotDePasseView(PasswordChangeView):
    template_name = "comptes/changer_mot_de_passe.html"
    form_class = ChangerMDPForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        self.request.user.doit_changer_mdp = False
        self.request.user.save()
        return super().form_valid(form)


def deconnexion(request):
    if request.method == "POST":
        logout(request)
        return redirect("connexion")
    return render(request, "workflow/dashboard.html")


# Create your views here.
