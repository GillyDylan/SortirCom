from django.shortcuts import render, redirect
from django.http import HttpResponse
from sortir.forms import ParticipantForm, ModParticipantForm, ConnexionForm, SortieForm
from sortir.models import Participant, Sortie, Site
from django.contrib.auth import hashers
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
        return render(request, 'sortir/accueil.html')


# Views pour le models Ville
# Views pour le models Lieu
# Views pour le models Site
# Views pour le models Sortie

def creersortie(request):
    sortie = Sortie()
    sortie.organisateur = Participant.objects.get(pk=request.session['userId'])
    form = SortieForm(request.POST or None, instance=sortie)

    if form.is_valid():
        sortie.save()
        return redirect('/Accueil/')

    context = {'form': form, 'villeOrga': sortie.organisateur.site.nom}
    return render(request, 'sortir/creerSortie.html', context)


def affichersortie(request, idsortie):
    sortie = Sortie.objects.get(pk=idsortie)
    context = {'sortie': sortie}
    return render(request, 'sortir/afficherSortie.html', context)


# A supprimer plus tard
def profil(request):
    if 'userId' not in request.session:
        form = ConnexionForm(request.POST or None)
        context = {'form': form}
        return render(request, 'sortir/connexion.html', context)
    else:
        return render(request, 'sortir/profil.html')


# Views lier le model Participant

def deconnexion(request):
    if request.session.__contains__('userId'):
        request.session.delete('userId')
        request.session.delete('isAdmin')

    form = ConnexionForm()
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def formulaireajouterparticipant(request):
    context = {'form': ParticipantForm()}
    return render(request, 'sortir/ajouterParticipant.html', context)


def connexion(request):
    form = ConnexionForm(request.POST or None)
    context = {'form': form}
    if 'userId' not in request.session:
        if form.is_valid():
            user = Participant.objects.filter(pseudo=form.cleaned_data['pseudo'])
            if hashers.check_password(form.cleaned_data['password'],user[0].password):
                if user.count() == 1:
                    print('connection')
                    request.session['userId'] = user[0].id
                    request.session['isAdmin'] = user[0].administrateur
                    if not form.cleaned_data.get('remember'):
                        form.request.session.set_expiry(0)
                    return render(request, 'sortir/accueil.html', )
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

    return redirect('accueil')


def modifierprofil(request):
    if request.session.__contains__('userId'):
        user = Participant.objects.get(pk=request.session['userId'])
        form = ModParticipantForm(request.POST or None, instance=user)
        if form.is_valid():
            user.password = hashers.make_password(user.password)
            user.save()

        context = {'user': user, 'form': form}
        return render(request, 'sortir/modifierProfil.html', context)

    return render(request, 'sortir/index.html')


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



