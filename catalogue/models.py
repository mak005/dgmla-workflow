from django.db import models

class Categorie(models.Model):
    code_categ = models.CharField(max_length=8, unique=True)
    libelle_categ = models.CharField(max_length=20)

    def __str__(self):
        return self.libelle_categ

class Article(models.Model):
    code_article = models.CharField(max_length=8, unique=True)
    libelle_article = models.CharField(max_length=30)
    quantite_stock = models.IntegerField()
    seuil_alerte = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.code_article:
            dernier = Article.objects.order_by('-id').first()
            prochain_numero = (dernier.id + 1) if dernier else 1
            self.code_article = f"ART{prochain_numero:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle_article

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
# Create your models here.
