import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sortir.forms import ParticipantForm, ConnexionForm, SortieForm
from sortir.forms import ParticipantForm, ModParticipantForm, ConnexionForm, SortieForm, AnnulerSortieForm
from sortir.models import Participant, Sortie, Site, Etat, Lieu
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
# Create your views here.


# Views pour charger la racine du site

def index(request):
    return render(request, 'sortir/index.html')


def accueil(request):
    if 'userId' not in request.session:
        form = ConnexionForm(request.POST or None)
        context = {'form': form}
        return render(request, 'sortir/connexion.html', context)
    else:
        sites = []
        for _site in Site.objects.all():
           sites.append(_site)
        user = Participant.objects.get(pk=request.session['userId'])
        context = {'sites': sites, 'user': user}
        return render(request, 'sortir/accueil.html', context)


# Views pour le models Ville
# Views pour le models Lieu
# Views pour le models Site
# Views pour le models Sortie
def ajouterparticipant(request):
    # if request.session.__contains__('userId'):
    #    user = Participant.objects.get(pk=request.session['userId'])
    #    if user.administrateur:
    user = Participant()
    form = ParticipantForm(data=(request.POST or None), instance=user)

    print(form.is_valid(), form.errors, type(form.errors))

    if form.is_valid():
        user.password = hashers.make_password(user.password)
        user.save()
        form = ParticipantForm()

    context = {'form': form}
    return render(request, 'sortir/ajouterParticipant.html', context)


def creersortie(request):
    sortie = Sortie()
    organisateur = Participant.objects.get(pk=request.session['userId'])
    form = SortieForm(request.POST or None, instance=sortie)

    print(form.is_valid(), form.errors, type(form.errors))

    if form.is_valid():
        sortie.save()
        return render(request, 'sortir/accueil.html')

    context = {'form': form, 'villeOrga': organisateur.site.nom}
    return render(request, 'sortir/creerSortie.html', context)


def affichersortie(request, idsortie):
    sortie = Sortie.objects.get(pk=idsortie)

    context = {'sortie': sortie}
    return render(request, 'sortir/afficherSortie.html', context)


def modifiersortie(request, idsortie):
    sortie = Sortie.objects.get(pk=idsortie)
    form = SortieForm(request.POST or None, instance=sortie)

    if form.is_valid():
        if 'Enregistrer' in request.POST:
            sortie.etat = Etat.objects.get(libelle='Créée')
            sortie.save()
        elif 'Publier' in request.POST:
            sortie.etat = Etat.objects.get(libelle='Ouverte')
            sortie.save()
        elif 'Supprimer' in request.POST:
            sortie.etat = Etat.objects.get(libelle='Ouverte')
            sortie.delete()

    context = {'form': form}
    return render(request, 'sortir/modifierSortie.html', context)


def annulersortie(request, idsortie):
    if 'userId' in request.session:
        sortie = Sortie.objects.get(pk=idsortie)
        if sortie.organisateur.id == request.session['userId']:
            form = AnnulerSortieForm(request.POST or None, instance=sortie)

            if form.is_valid():
                sortie.etat = Etat.objects.get(libelle='Annuler')
                sortie.save()
                return accueil(request)

            context = {'form': form, 'sortie': sortie}
            return render(request, 'sortir/annulerSortie.html', context)

    return connexion(request)
# Views lier le model Participant


def deconnexion(request):
    if 'userId' in request.session:
        del request.session['userId']
        del request.session['isAdmin']
        print('deconnecté')
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def formulaireajouterparticipant(request):
    context = {'form': ParticipantForm()}
    return render(request, 'sortir/ajouterParticipant.html', context)


def connexion(request):
    anciennePage = request.headers["Referer"][request.headers["Referer"].rfind('/')+1:]
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    if 'userId' not in request.session:
        if form.is_valid():
            user = Participant.objects.filter(pseudo=form.cleaned_data['pseudo'])
            if hashers.check_password(form.cleaned_data['password'], user[0].password):
                if user.count() == 1:
                    print('connection')
                    request.session['userId'] = user[0].id
                    request.session['isAdmin'] = user[0].administrateur
                    if not form.cleaned_data.get('remember'):
                        request.session.set_expiry(0)
                    if anciennePage == "Profil":
                        user = Participant.objects.get(pk=request.session['userId'])
                        form = ParticipantForm(request.GET or None, instance=user)
                        context = {'user': user, 'form': form}
                        return render(request, 'sortir/modifierProfil.html', context)
                    elif anciennePage == "Sites" and user[0].administrateur:
                        return sites(request)
                    elif anciennePage == "Villes" and user[0].administrateur:
                        return villes(request)
                    elif anciennePage == "Participants" and user[0].administrateur:
                        return participants(request)
                    else:
                        return accueil(request)
    return render(request, 'sortir/connexion.html', context)


def afficherprofil(request, idOrganisateur):
    if request.session.__contains__('userId'):
    #    sortie = Sortie.objects.get(pk=idSortie)
    #    if sortie.get(organisateur=idOrganisateur) is not None &
    #            sortie.participants.get(id=request.session['userId'])) is not None:
            participant = Participant.objects.get(pk=idOrganisateur)
            if participant != None:
                context = {'user': participant}
                return render(request, 'sortir/afficherProfil.html', context)

    return connexion(request)


def modifierprofil(request):
    if 'userId' in request.session:
        user = Participant.objects.get(pk=request.session['userId'])
        form = ModParticipantForm(request.POST or None, instance=user)
        if form.is_valid():
            user.password = hashers.make_password(user.password)
            user.save()

        context = {'user': user, 'form': form}
        return render(request, 'sortir/modifierProfil.html', context)

    return connexion(request)


def sites(request):
    if 'userId' in request.session:
        user = Participant.objects.get(pk=request.session['userId'])
        context = {'user': user}
        if user.administrateur:
            return render(request, 'sortir/sites.html', context)
        else:
            return accueil(request)
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def villes(request):
    if 'userId' in request.session:
        user = Participant.objects.get(pk=request.session['userId'])
        context = {'user': user}
        if user.administrateur:
            return render(request, 'sortir/villes.html', context)
        else:
            return accueil(request)
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def participants(request):
    if 'userId' in request.session:
        user = Participant.objects.get(pk=request.session['userId'])
        context = {'user': user}
        if user.administrateur:
            return render(request, 'sortir/participants.html', context)
        else:
            return accueil(request)
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def getsession(request):
    if 'userId' in request.session:
        user = Participant.objects.get(pk=request.session['userId'])
        data = {
            'userId': user.id,
            'isAdmin': user.administrateur
        }
    else:
        data = {
            'userId': 0,
            'isAdmin': False
        }
    return JsonResponse(data)


def getsorties(request):
    sorties = Sortie.objects.all()
    data = {
        'sorties': json.dumps(list(sorties.values('id',
                                                  'nom',
                                                  'dateHeureDebut',
                                                  'dateHeureFin',
                                                  'dateLimiteInscription',
                                                  'nbinscriptionMax',
                                                  'etat_id',
                                                  'etat__libelle',
                                                  'lieu_id',
                                                  'lieu__nom',
                                                  'organisateur__site_id',
                                                  'organisateur_id',
                                                  'organisateur__nom')),
                              cls=DjangoJSONEncoder),
        'participants': json.dumps(list(sorties.values('id',
                                                       'participants__site_id',
                                                       'participants__nom',
                                                       'participants__prenom')),
                                   cls=DjangoJSONEncoder),
        'userId': request.session['userId']
    }
    return JsonResponse(data)


def getlieux(request):
    lieux = Lieu.objects.all()
    data = {
        'lieux': json.dumps(list(lieux.values('id',
                                              'nom',
                                              'rue',
                                              'latitude',
                                              'longitude',
                                              'ville_id',
                                              'ville__codePostal')),
                            cls=DjangoJSONEncoder),
    }
    return JsonResponse(data)




