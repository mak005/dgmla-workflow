from pyexpat.errors import messages

from django.shortcuts import redirect, render, get_object_or_404
from .models import Article, Categorie
from django.contrib.auth.decorators import login_required, user_passes_test


# Récupération des données à afficher

@login_required
def catalogue(request):
    categorie_id = request.GET.get("categorie", "")
    articles = Article.objects.all()
    if categorie_id:
        articles = articles.filter(categorie_id=categorie_id)
    categories = Categorie.objects.all()
    return render(
        request,
        "catalogue/catalogue.html",
        {
            "articles": articles,
            "categories": categories,
            "categorie_selectionnee": int(categorie_id) if categorie_id else None,
        },
    )


def est_gestionnaire_dgmla(user):
    return user.role == "GEST_DGMLA"


# Traitement du formulaire d'ajout de catégorie

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def ajouter_categorie(request):
    if request.method == "POST":
        code = request.POST.get("code_categ").strip()
        libelle = request.POST.get("libelle_categ").strip()

        if code and libelle:
            Categorie.objects.create(code_categ=code, libelle_categ=libelle)
        else:
            messages.error(request, "Le code et le libellé sont obligatoires.")
    return redirect("catalogue")


# Traitement du formulaire de modification de catégorie

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def modifier_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == "POST":
        categorie.code_categ = request.POST.get("code_categ")
        categorie.libelle_categ = request.POST.get("libelle_categ")

        categorie.save()
        return redirect("catalogue")
    return render(request, "catalogue/catalogue.html", {"categorie": categorie})


# Traitement du formulaire d'ajout d'article

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def ajouter_article(request):
    if request.method == "POST":
        libelle = request.POST.get("libelle_article").strip()
        id_categ = request.POST.get("categorie").strip()
        quantite_stock = request.POST.get("quantite_stock").strip()
        seuil_alerte = request.POST.get("seuil_alerte").strip()

        if libelle and id_categ and quantite_stock and seuil_alerte:
            Article.objects.create(
                libelle_article=libelle,
                categorie=id_categ,
                quantite_stock=quantite_stock,
                seuil_alerte=seuil_alerte,
            )
    return redirect("catalogue")


# Traitement du formulaire de modification d'article

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def modifier_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.libelle_article = request.POST.get("libelle_article")
        article.categorie_id = request.POST.get("categorie")
        article.quantite_stock = int(request.POST.get("quantite_stock"))
        article.seuil_alerte = int(request.POST.get("seuil_alerte"))

        article.save()
        return redirect("catalogue")
    return render(request, "catalogue/catalogue.html", {"article": article})


# Traitement du formulaire de suppression de catégorie

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == "POST":
        categorie.delete()
    return redirect("catalogue")


# Traitement du formulaire de suppression d'article

@login_required
@user_passes_test(est_gestionnaire_dgmla)
def supprimer_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.delete()
    return redirect("catalogue")


# Create your views here.
