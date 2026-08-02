from datetime import datetime, timedelta, timezone
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms
from comptes.models import Agent


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Matricule",
        widget=forms.TextInput(
            attrs={
                "class": "w-full border-0 border-b border-b-gray-500 pb-2 px-0 bg-transparent focus:outline-none focus:border-red-500 disabled:opacity-50 disabled:cursor-not-allowed",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border-0 border-b border-b-gray-500 pb-2 focus:outline-none focus:border-red-500 disabled:opacity-50 disabled:cursor-not-allowed",
            }
        ),
    )

    # Message d'erreur standard
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Matricule ou mot de passe incorrect.",
    }

    def clean(self):  # Récupération des infos de connexion
        matricule = self.cleaned_data.get("username")
        self.password = self.cleaned_data.get("password")

        agent = None

        # Récupération de l'objet agent s'il existe
        if matricule:
            agent = Agent.objects.filter(
                matricule=matricule
            ).first()  # Filtrage par matricule (select where matricule = matricule récupéré au préalable)

            if agent and agent.bloque_jusqu_a:
                if agent.bloque_jusqu_a < datetime.now(timezone.utc):
                    agent.bloque_jusqu_a = None
                    agent.save()
                else:
                    secondes = int(
                        (
                            agent.bloque_jusqu_a - datetime.now(timezone.utc)
                        ).total_seconds()
                    )
                    raise forms.ValidationError(
                        f"Compte temporairement bloqué: Réessayez dans {secondes} secondes."
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
                    agent.save()
                    raise forms.ValidationError(
                        "Ce compte est bloqué. Veuillez contacter l'administrateur IT.",
                        code="compte_bloque",
                    )

                # Blocage temporaire
                elif agent.nombre_tentatives_connexion == 3:
                    agent.bloque_jusqu_a = datetime.now(timezone.utc) + timedelta(
                        seconds=90
                    )
                    agent.save()
                    # Message d'erreur
                    raise forms.ValidationError(
                        f"Compte temporairement bloqué. Réessayez dans 90 secondes.",
                        code="compte_temporairement_bloque",
                    )
                agent.save()
            elif agent and agent.est_bloque:
                raise forms.ValidationError(
                    "Ce compte est bloqué. Veuillez contacter l'administrateur IT.",
                    code="compte_bloque",
                )
            raise

        # Authentification réussie
        user = self.get_user()
        if user:
            user.nombre_tentatives_connexion = 0
            user.bloque_jusqu_a = None
            user.save()

        return cleaned_data


class ChangerMDPForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border-0 border-b border-b-gray-500 pb-2 focus:outline-none focus:border-red-500",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border-0 border-b border-b-gray-500 pb-2 focus:outline-none focus:border-red-500",
            }
        ),
        help_text="Votre mot de passe doit contenir au moins : 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.",
    )
    new_password2 = forms.CharField(
        label="Confirmez le nouveau mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border-0 border-b border-b-gray-500 pb-2 focus:outline-none focus:border-red-500",
            }
        ),
    )
