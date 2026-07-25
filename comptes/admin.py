from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Agent, Departement

class AgentAdmin(UserAdmin):
    model = Agent
    list_display = ('matricule', 'email', 'role', 'departement', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('matricule', 'first_name', 'last_name', 'role', 'departement')}),
        ('Sécurité', {'fields': ('nombre_tentatives_connexion', 'est_bloque', 'doit_changer_mdp')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricule', 'email', 'role', 'departement', 'password1', 'password2'),
        }),
    )
    ordering = ('matricule',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Departement)

# Register your models here.
