from django import forms
from django.core.validators import RegexValidator
from sortir.models import Site, Lieu, Ville
import datetime


class ParticipantForm(forms.Form):
    pseudo = forms.CharField(min_length=3, max_length=50, required=True, label='Pseudo :')
    email = forms.EmailField(max_length=100, required=True, label='E-mail :')
    nom = forms.CharField(min_length=2, max_length=50, required=True, label='Nom :')
    prenom = forms.CharField(min_length=2, max_length=50, required=True, label='Prenom :')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=100, required=True, label='Mot de Passe :')
    confirmPassword = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=100, required=True, label='Confirmer mdp :')
    telephone = forms.CharField(validators=[RegexValidator(r'^\d{10}$')], min_length=10, max_length=10, required=True, label='Téléphone :')
    site = forms.ModelChoiceField(queryset=Site.objects.all(), empty_label=None, required=True, label='Site rataché :')
    administrateur = forms.BooleanField(required=False, label='Est administrateur :')
    actif = forms.BooleanField(required=False, label='Est actif :')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirmPassword')
        if password != conf_password:
            raise forms.ValidationError("Attention : Mot de passe et confirmation différents")


class SortieForm(forms.Form):
    nom = forms.CharField(min_length=2, max_length=50, required=True, label='Nom Sortie :')
    dateHeureDebut = forms.DateTimeField(required=True, label='Date début de l\'évenement :')
    dateHeureFin = forms.DateTimeField(required=True, label='Date fin de l\'évenement :')
    dateLimiteInscription = forms.DateField(required=True, label='Date limite d\'inscription :')
    nbInscriptionMax = forms.IntegerField(min_value=1, required=True, label='Participants maximum :')
    infosSortie = forms.CharField(widget=forms.Textarea, required=True, label='infos :')
    lieu = forms.ModelChoiceField(queryset=Lieu.objects.all(), empty_label=None, required=True, label='Lieu :')

    def clean_dateLimiteInscription(self):
        datelimite = self.cleaned_data.get('dateLimiteInscription')
        datejour = datetime.datetime.now()
        if datelimite <= datejour:
            raise forms.ValidationError("Attention : La date limite doit etre postérieur à aujourd'hui")

    def clean_dateHeureDebut(self):
        datedebut = self.cleaned_data.get('dateHeureDebut')
        datelimite = self.cleaned_data.get('dateLimiteInscription')
        datejour = datetime.datetime.now()
        if datedebut < datelimite.hour + 1:
            raise forms.ValidationError("Attention : La date de début "
                                        "doit etre postérieur à la date de fin d'inscription")
        if datedebut < datejour:
            raise forms.ValidationError("Attention : La date de début doit etre postérieur à aujourd'hui")

    def clean_dateHeureFin(self):
        datedebut = self.cleaned_data.get('dateHeureDebut')
        datefin = self.cleaned_data.get('dateHeureFin')
        if datefin <= datedebut:
            raise forms.ValidationError("Attention : la date et l'heure de fin "
                                        "doivent être postérieur à la date de début")


class SiteForm(forms.Form):
    nom = forms.CharField(min_length=2, max_length=50, required=True, label=None)


class VilleForm(forms.Form):
    nom = forms.CharField(min_length=2, max_length=50, required=True, label=None)
    codePostal = forms.CharField(min_length=5, max_length=5, validators=[RegexValidator(r'^\d{5}$')])


class LieuForm(forms.Form):
    nom = forms.CharField(min_length=2, max_length=50, required=True, label='Nom lieu :')
    rue = forms.CharField(min_length=2, max_length=50, required=True, label='rue lieu :')
    latitude = forms.FloatField(required=True, label='latitude :')
    longitude = forms.FloatField(required=True, label='longitude :')
    ville = forms.ModelChoiceField(queryset=Ville.objects.all(), required=True, label='Ville :')


class ConnexionFor(forms.Form):
    pseudo = forms.CharField(min_length=3, max_length=50, required=True, label='Pseudo :')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=100, required=True, label='Mot de Passe :')
    administrateur = forms.BooleanField(required=False, label='Se souvenir de moi ?')
