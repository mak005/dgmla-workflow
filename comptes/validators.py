import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def validate(self, password, user=None):

        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_\-]{12,}$"

        if not re.match(regex, password):
            raise ValidationError(
                "Le mot de passe doit contenir au moins : "
                "12 caractères, une majuscule, une minuscule, "
                "un chiffre et un caractère spécial."
            )

    def get_help_text(self):
        return (
            "Au moins 12 caractères, une majuscule, une minuscule, "
            "un chiffre et un caractère spécial."
        )
