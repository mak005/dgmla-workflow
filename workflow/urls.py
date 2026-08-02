from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("demande/creer/", views.creer_demande, name="creer_demande"),
    path(
        "articles/<int:categorie_id>/",
        views.articles_par_categorie,
        name="articles_par_categorie",
    ),
    path(
        "demande/details/<int:id>/", views.consulter_demande, name="consulter_demande"
    ),
    path("demande/modifier/<int:id>/", views.modifier_demande, name="modifier_demande"),
    path("demandes/a_examiner/", views.demandes_a_examiner, name="demandes_a_examiner"),
    path("demande/valider/<int:id>/", views.valider_demande, name="valider_demande"),
    path("demande/rejeter/<int:id>/", views.rejeter_demande, name="rejeter_demande"),
]
