from django.shortcuts import render, redirect, get_object_or_404
from .models import Demande, Article, LigneDemande
from comptes.models import Agent, Departement
from catalogue.models import Categorie
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from datetime import datetime, timezone
from django.contrib import messages
from django.db import transaction


def dashboard(request):
    demandes = Demande.objects.filter(agent=request.user)
    statuts_tuples = Demande.Statut.choices

    # Recuperation des statuts
    statuts = []
    for statut in statuts_tuples:
        statuts.append(statut[0])

    # Filtrage des demandes selon le statut selectionne
    statut_selectionne = request.GET.get("statut", "")
    if statut_selectionne:
        demandes = demandes.filter(statut=statut_selectionne)

    return render(
        request,
        "workflow/dashboard.html",
        {
            "demandes": demandes,
            "statuts": statuts,
            "statut_selectionne": statut_selectionne if statut_selectionne else None,
        },
    )


@login_required
def creer_demande(request):
    categories = Categorie.objects.all()
    articles = Article.objects.all()

    if request.method == "POST":

        # Creation de la demande a la soumission du formulaire
        demande = Demande.objects.create(
            date_demande=datetime.now(timezone.utc), agent=request.user
        )

        # Récupération du nombre de lignes
        nbrLignes = int(request.POST.get("form-TOTAL_FORMS", 0))

        # Si aucune ligne n'est créée
        if nbrLignes == 0:
            demande.delete()
            return redirect("dashboard")

        # Creation des lignes de demande
        for i in range(1, nbrLignes + 1):
            article_id = request.POST.get(f"form-{str(i)}-article")
            if not article_id:
                continue

            quantite_demandee = int(
                request.POST.get(f"form-{str(i)}-quantite_demandee")
            )

            LigneDemande.objects.create(
                demande=demande,
                article_id=article_id,
                quantite_demandee=quantite_demandee,
            )
            messages.success(request, "Votre demande a bien été envoyée.")
        return redirect("dashboard")
    return render(
        request,
        "workflow/creer_demande.html",
        {
            "categories": categories,
            "articles": articles,
        },
    )


# Filtrage des articles par categorie dans le formulaire de demande
def articles_par_categorie(request, categorie_id):
    articles = Article.objects.filter(categorie_id=categorie_id)
    return JsonResponse(list(articles.values("id", "libelle_article")), safe=False)


# Consultation d'une demande
@login_required
def consulter_demande(request, id):
    demande = get_object_or_404(Demande, id=id)
    lignesDemande = LigneDemande.objects.filter(demande_id=id)

    return render(
        request,
        "workflow/details_demande.html",
        {"demande": demande, "lignes": lignesDemande},
    )


# Modification d'une demande
@login_required
def modifier_demande(request, id):
    demande = get_object_or_404(Demande, id=id)
    lignesDemande = LigneDemande.objects.filter(demande_id=id)
    categories = Categorie.objects.all()
    articles = Article.objects.all()

    if request.method == "POST":
        nbrLignes = int(
            request.POST.get("form-TOTAL_FORMS", 0)
        )  # Récupération du nombre de lignes

        # Si aucune ligne n'est créée
        if nbrLignes == 0:
            messages.error(request, "Une demande doit contenir au moins un article.")
            return redirect("modifier_demande", id=id)

        with transaction.atomic():
            lignesDemande.delete()  # suppression des anciennes lignes
            for i in range(1, nbrLignes + 1):
                article_id = request.POST.get(f"form-{str(i)}-article")
                quantite_demandee = request.POST.get(f"form-{str(i)}-quantite_demandee")

                # Verification article selectionne
                if not article_id:
                    continue
                # Verification quantite selectionnee
                if not quantite_demandee:
                    continue
                quantite_demandee = int(quantite_demandee)

                # Recréation de la ligne
                LigneDemande.objects.create(
                    demande=demande,
                    article_id=article_id,
                    quantite_demandee=quantite_demandee,
                )
            messages.success(request, "Votre demande a bien été modifiée.")
        return redirect("dashboard")
    return render(
        request,
        "workflow/modifier_demande.html",
        {
            "demande": demande,
            "lignes": lignesDemande,
            "categories": categories,
            "articles": articles,
        },
    )


def est_responsable_departement(user):
    return user.role == "RESP_DEPT"


@login_required
@user_passes_test(est_responsable_departement)
def demandes_a_examiner(request):
    demandes = Demande.objects.all()

    return render(request, "workflow/demandes_a_examiner.html", {"demandes": demandes})


def valider_demande(request, id):
    demande = get_object_or_404(Demande, id=id)

    if request.method == "POST":
        demande.statut = demande.Statut.VALIDEE
        return redirect("demandes_a_examiner")
    return render(request, "valider_demande")


def rejeter_demande(request, id):
    pass


# Create your views here.
