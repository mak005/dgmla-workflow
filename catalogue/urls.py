from django.urls import path
from . import views

urlpatterns = [
    path("catalogue/", views.catalogue, name="catalogue"),
    path("categorie/ajouter/", views.ajouter_categorie, name="ajouter_categorie"),
    path(
        "categorie/modifier/<int:id>/",
        views.modifier_categorie,
        name="modifier_categorie",
    ),
    path("article/ajouter/", views.ajouter_article, name="ajouter_article"),
    path("article/modifier/<int:id>/", views.modifier_article, name="modifier_article"),
    path("categorie/supprimer/<int:id>/", views.supprimer_categorie, name="supprimer_categorie"),
    path("article/supprimer/<int:id>/", views.supprimer_article, name="supprimer_article"),
]
