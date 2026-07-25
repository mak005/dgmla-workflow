from django.db import models
from comptes.models import Agent
from catalogue.models import Article

class Demande(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente' # statut par défaut
        VALIDEE = 'VALIDEE', 'Validée' # après validation par le responsable département
        REJETEE = 'REJETEE', 'Rejetée' # après rejet par le responsable département
        TRANSMISE = 'TRANSMISE', 'Transmise' # après transmission au DGMLA suite à la validation par le responsable département
        EN_PREPARATION = 'EN_PREPARATION', 'En préparation' # après modification du statut par le gestionnaire DGMLA
        PREPAREE = 'PREPAREE', 'Préparée' # après préparation des fournitures et en attente de validation par le responsable DGMLA
        PRETE = 'PRETE', 'Prête' # après validation par le responsable DGMLA 
        LIVREE = 'LIVREE', 'Livrée' # après livraison des fournitures, modification du statut par le responsable département

    date_demande = models.DateField()
    date_livraison = models.DateField()
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.EN_ATTENTE)
    motif_rejet = models.TextField(null=True, blank=True)

    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)

    def __str__(self):
        return f"DEM-{self.id:04d}"

class LigneDemande(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    quantite_demandee = models.IntegerField()
    quantite_servie = models.IntegerField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('demande', 'article')
    
# Create your models here.
