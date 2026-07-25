from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class AgentManager(BaseUserManager):
    def create_user(self, matricule, email, password=None, **extra_fields):
        if not matricule:
            raise ValueError("Le matricule est obligatoire")
        email = self.normalize_email(email)

        departement = extra_fields.pop("departement", None)

        agent = self.model(matricule=matricule, email=email, **extra_fields)
        if departement is not None:
            agent.departement_id = departement
        agent.set_password(password)
        agent.save(using=self._db)
        return agent

    def create_superuser(self, matricule, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(matricule, email, password, **extra_fields)


class Departement(models.Model):
    code_dept = models.CharField(max_length=6, unique=True)
    libelle_dept = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.code_dept


class Agent(AbstractUser):
    objects = AgentManager()

    class Role(models.TextChoices):
        AGENT = "AGENT", "Agent de département"
        RESP_DEPT = "RESP_DEPT", "Responsable de département"
        RESP_DGMLA = "RESP_DGMLA", "Responsable DGMLA"
        GEST_DGMLA = "GEST_DGMLA", "Gestionnaire DGMLA"
        ADMIN_IT = "ADMIN_IT", "Administrateur IT"

    username = None
    matricule = models.CharField(max_length=4, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.AGENT)

    doit_changer_mdp = models.BooleanField(default=True)
    nombre_tentatives_connexion = models.IntegerField(default=0)
    est_bloque = models.BooleanField(default=False)
    bloque_jusqu_a = models.DateTimeField(null=True, blank=True)

    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)

    USERNAME_FIELD = "matricule"
    REQUIRED_FIELDS = ["email", "departement"]

    def save(self, *args, **kwargs):
        if self.role in [self.Role.RESP_DGMLA, self.Role.GEST_DGMLA]:
            dgmla, _ = Departement.objects.get_or_create(
                code_dept='DGMLA',
                defaults={'libelle_dept': 'Moyens Généraux, Logistique et Achats'}
            )
            self.departement = dgmla
        super().save(*args, **kwargs)


# Create your models here.
