from django import forms
from django.core.validators import RegexValidator
from sortir.models import Sortie, Site, Lieu, Ville, Participant
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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


class ModParticipantForm(SuperParticipantForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput, required=False, max_length=100, label='Confirmer :')

    class Meta(SuperParticipantForm.Meta):
        fields = SuperParticipantForm.Meta.fields + ['confirmPassword']

    def __init__(self, *args, **kwargs):
        super(ModParticipantForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirmPassword')
        if password != conf_password:
            raise forms.ValidationError("Attention : Mot de passe et confirmation différents")
        return cleaned_data


class SortieForm(forms.ModelForm):
    ville = forms.ModelChoiceField(queryset=Ville.objects.all(), required=False)

    class Meta:
        model = Sortie
        fields = ['nom', 'dateHeureDebut', 'dateHeureFin', 'dateLimiteInscription', 'infosSortie', 'lieu', 'nbinscriptionMax']
        labels = {
            'dateHeureDebut': _('Date debut :'),
            'dateHeureFin': _('Date fin :'),
            'dateLimiteInscription': _('Date fin inscription :'),
            'infosSortie': _('Description et infos :'),
            'nbinscriptionMax': _('Nombre maximum de participant :'),
        }
        widgets = {
            'dateHeureDebut': forms.DateTimeInput(attrs={'placeholder': 'dd/mm/yyyy hh:mm', 'id': 'form_datetime1'}),
            'dateHeureFin': forms.DateTimeInput(attrs={'placeholder': 'dd/mm/yyyy hh:mm', 'id': 'form_datetime2'}),
            'dateLimiteInscription': forms.DateTimeInput(attrs={'placeholder': 'dd/mm/yyyy', 'id': 'form_datetime3'})
        }

    def clean(self):
        print("Je suis dans le clean")
        cleaned_data = super().clean()
        print("Supeer clean passé")
        datedebut = self.cleaned_data.get('dateHeureDebut')
        datelimite = self.cleaned_data.get('dateLimiteInscription')
        datejour = datetime.now()
        datefin = self.cleaned_data.get('dateHeureFin')
        print("J'ai réussi a recuperer les données")
        if datelimite <= datejour.date():
            raise forms.ValidationError("Attention : La date limite doit etre postérieur à aujourd'hui")
        print("Test 1 passé")
        if datedebut.date() < datelimite:
            raise forms.ValidationError("Attention : La date de début "
                                        "doit etre postérieur à la date de fin d'inscription")
        print("Test 2 passé")
        if datedebut.date() < datejour.date():
            raise forms.ValidationError("Attention : La date de début doit etre postérieur à aujourd'hui")
        print("Test 3 passé")
        if datefin <= datedebut:
            raise forms.ValidationError("Attention : la date et l'heure de fin "
                                        "doivent être postérieur à la date de début")
        print("Test 4 passé")
        return cleaned_data


class AnnulerSortieForm(forms.ModelForm):
    class Meta:
        model = Sortie
        fields = ['motif_annulation']

    def clean(self):
        cleaned_data = super().clean()
        if len(self.cleaned_data['motif_annulation'].strip()) == 0:
            raise forms.ValidationError("Le motif ne doit pas être vide")
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
        fields = ['nom', 'ville', 'rue', 'latitude', 'longitude']


class ConnexionForm(forms.Form):
    pseudo = forms.CharField(min_length=3, max_length=50, required=True, label='Pseudo :')
    password = forms.CharField(widget=forms.PasswordInput, min_length=1, max_length=100, required=True, label='Mot de Passe :')
    remember = forms.BooleanField(required=False, label='Se souvenir de moi ?')
