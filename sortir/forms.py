from django import forms
from django.core.validators import RegexValidator
from sortir.models import Sortie, Site, Lieu, Ville, Participant
import datetime


class SuperParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ['pseudo', 'nom', 'prenom', 'email', 'telephone', 'site', 'administrateur', 'actif', 'password']
        widgets = {
            'password': forms.PasswordInput
        }


class ParticipantForm(SuperParticipantForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=100, required=True, label='Confirmer :')

    class Meta(SuperParticipantForm.Meta):
        fields = SuperParticipantForm.Meta.fields + ['confirmPassword']

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirmPassword')
        if password != conf_password:
            raise forms.ValidationError("Attention : Mot de passe et confirmation différents")
        return cleaned_data


class SortieForm(forms.ModelForm):

    class Meta:
        model = Sortie
        fields = ['nom', 'dateHeureDebut', 'dateHeureFin', 'dateLimiteInscription', 'infosSortie', 'lieu', 'nbinscriptionMax']

    def clean(self):
        cleaned_data = super().clean()
        datedebut = self.cleaned_data.get('dateHeureDebut')
        datelimite = self.cleaned_data.get('dateLimiteInscription')
        datejour = datetime.datetime.now()
        datefin = self.cleaned_data.get('dateHeureFin')

        if datelimite <= datejour:
            raise forms.ValidationError("Attention : La date limite doit etre postérieur à aujourd'hui")

        if datedebut < datelimite.hour + 1:
            raise forms.ValidationError("Attention : La date de début "
                                        "doit etre postérieur à la date de fin d'inscription")
        if datedebut < datejour:
            raise forms.ValidationError("Attention : La date de début doit etre postérieur à aujourd'hui")

        if datefin <= datedebut:
            raise forms.ValidationError("Attention : la date et l'heure de fin "
                                        "doivent être postérieur à la date de début")

        return cleaned_data


class SiteForm(forms.ModelForm):

    class Meta:
        model = Site
        fields = ['nom']


class VilleForm(forms.ModelForm):

    class Meta:
        model = Ville
        fields = ['nom', 'codePostal']


class LieuForm(forms.ModelForm):

    class Meta:
        model = Lieu
        fields = ['nom', 'codePostal']


class ConnexionForm(forms.Form):
    pseudo = forms.CharField(min_length=3, max_length=50, required=True, label='Pseudo :')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=100, required=True, label='Mot de Passe :')
    remember = forms.BooleanField(required=False, label='Se souvenir de moi ?')
