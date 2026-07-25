from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Demande, Article
from catalogue.models import Categorie
from django.contrib.auth.decorators import login_required


class DashboardView(TemplateView):
    template_name = "workflow/dashboard.html"

    def dashboard(request):
        demandes = Demande.objects.all()
        statuts = ["En attente", "Validée", "Rejetée"]
        return render(
            request,
            "workflow/dashboard.html",
            {"demandes": demandes, "statuts": statuts},
        )


# Traitement du formulaire de création de demande


@login_required
def creer_demande(request):
    categories = Categorie.objects.all()
    articles = Article.objects.all()

    return render(
        request,
        "workflow/creer_demande.html",
        {
            "categories": categories,
            "articles": articles,
        },
    )


def consulter_demande(request):
    # demande = get_object_or_404(Demande, id=id)

    # return render(request, 'workflow/details_demande.html', {'demande': demande})
    return render(request, "workflow/details_demande.html")


# Create your views here.
