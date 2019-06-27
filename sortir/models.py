from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.


class Ville(models.Model):
    nom = models.CharField(unique=True, blank=False, max_length=100)
    codePostal = models.CharField(blank=False, max_length=5, validators=[RegexValidator(r'^\d{5}$')])


class Lieu(models.Model):
    nom = models.CharField(unique=True, blank=False, max_length=100)
    rue = models.CharField(unique=True, blank=False, max_length=100)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)


class Etat(models.Model):
    libelle = models.CharField(blank=False, max_length=20)


class Site(models.Model):
    nom = models.CharField(unique=True, blank=False, max_length=50)


class Participant(models.Model):
    pseudo = models.CharField(unique=True, blank=False, max_length=50)
    nom = models.CharField(blank=False, max_length=50)
    prenom = models.CharField(blank=False, max_length=50)
    email = models.EmailField(unique=True, blank=False, max_length=100)
    password = models.CharField(blank=False, max_length=100)
    telephone = models.CharField(blank=False,  max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    administrateur = models.BooleanField(default=False)
    actif = models.BooleanField(default=True)
    site = models.ForeignKey(Site, blank=False, on_delete=models.PROTECT)


class Sortie(models.Model):
    nom = models.CharField(blank=False, max_length=100)
    dateHeureDebut = models.DateTimeField(blank=False)
    dateHeureFin = models.DateTimeField(blank=False)
    dateLimiteInscription = models.DateField(blank=False)
    nbinscriptionMax = models.PositiveSmallIntegerField(blank=False)
    infosSortie = models.TextField(blank=False)
    lieu = models.ForeignKey(Lieu, blank=False, null=True, on_delete=models.SET_NULL)
    etat = models.ForeignKey(Etat, blank=False, on_delete=models.PROTECT)
    organisateur = models.ForeignKey(Participant, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant, related_name='sorties', blank=True)
