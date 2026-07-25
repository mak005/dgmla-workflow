from datetime import datetime, timedelta, timezone
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms

from comptes.models import Agent


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Matricule : ",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Matricule",
                "class": "w-full border-0 border-b border-b-gray-500 py-2 px-0 bg-transparent focus:outline-none focus:border-red-500 placeholder-gray-600",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe : ",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "w-full border-0 border-b border-b-gray-500 py-2 focus:outline-none focus:border-red-500 placeholder-gray-600",
            }
        ),
    )

    # Message d'erreur standard
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': "Matricule ou mot de passe incorrect.",
    }

    def clean(self): # Récupération des infos de connexion
        matricule = self.cleaned_data.get('username')
        self.password = self.cleaned_data.get('password')

        agent = None
        
        # Récupération de l'objet agent s'il existe
        if matricule:
            agent = Agent.objects.filter(matricule=matricule).first() # Filtrage par matricule (select where matricule = matricule récupéré au préalable)

        if agent:
        
            # Message d'erreur affiché en cas de blocage permanent 
            if agent.est_bloque:
                raise forms.ValidationError(
                    "Ce compte est bloqué. Veuillez contacter l'administrateur IT.",
                    code='compte_bloque',
                )
            
            # Message d'erreur affiché en cas de blocage temporaire
            if agent.bloque_jusqu_a and agent.bloque_jusqu_a > datetime.now(timezone.utc):
                secondes = int((agent.bloque_jusqu_a - datetime.now(timezone.utc)).total_seconds())
                raise forms.ValidationError(
                    f"Compte temporairement bloqué. Réessayez dans {secondes} secondes.",
                    code='compte_temporairement_bloque',
                )

        try:
            cleaned_data = super().clean() 
        except forms.ValidationError:

        # Authentification non réussie
            if agent and not agent.est_bloque:
                agent.nombre_tentatives_connexion += 1

                # Blocage permanent
                if agent.nombre_tentatives_connexion >= 6:
                    agent.est_bloque = True
                    agent.bloque_jusqu_a = None

                # Blocage temporaire
                elif agent.nombre_tentatives_connexion == 3:
                    agent.bloque_jusqu_a = datetime.now(timezone.utc) + timedelta(seconds=90)
                agent.save()
            raise

        # Authentification réussie
        if self.get_user():
            user = self.get_user()
            user.nombre_tentatives_connexion = 0
            user.bloque_jusqu_a = None
            user.save()

        return cleaned_data
    

class ChangerMDPForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien mot de passe : ",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ancien mot de passe",
                "class": "w-full border-0 border-b border-b-gray-500 py-2 focus:outline-none focus:border-red-500 placeholder-gray-600",
            }
        ),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Nouveau mot de passe",
                "class": "w-full border-0 border-b border-b-gray-500 py-2 focus:outline-none focus:border-red-500 placeholder-gray-600",
            }
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmez le nouveau mot de passe",
                "class": "w-full border-0 border-b border-b-gray-500 py-2 focus:outline-none focus:border-red-500 placeholder-gray-600",
            }
        )
    )
