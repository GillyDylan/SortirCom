from django.shortcuts import render, redirect
from django.http import HttpResponse
from sortir.forms import ParticipantForm, ConnexionForm, VilleForm, SortieForm
from sortir.models import Participant, Ville, Sortie, Site
from django.contrib.auth import hashers
# Il faudra réorganiser les fonctions pour plus de lisibilité

# Views pour charger la racine du site

def index(request):
    return render(request, 'sortir/index.html')


def accueil(request):
    print('couille')
    return render(request, 'sortir/accueil.html')

# Views pour le models Ville
# Views pour le models Lieu
# Views pour le models Site
# Views pour le models Sortie

def creerSortie(request):
    sortie = Sortie()
    form = SortieForm(request.POST or None, instance=sortie)

    if form.is_valid():
        sortie.save()
        return redirect('/Accueil/')

    context = {'form': form}
    return render(request, 'sortir/creerSortie.html', context)

# A supprimer plus tard
def profil(request):
    return render(request, 'sortir/profil.html')
######

# Views lier le model Participant

def deconnexion(request):
    if request.session.__contains__('userId'):
        request.session.delete('userId')

    form = ConnexionForm()
    context = {'form': form}
    return render(request, 'sortir/connexion.html', context)


def formulaireajouterparticipant(request):
    context = {'form': ParticipantForm()}
    return render(request, 'sortir/ajouterParticipant.html', context)


def connexion(request):
    form = ConnexionForm(request.POST or None)
    if form.is_valid():
        user = Participant.objects.filter(pseudo=form.cleaned_data['pseudo'])
        if hashers.check_password(form.cleaned_data['password'], user[0].password):
            request.session['userId'] = user[0].id
            print(request.session.get('userId'))
            return redirect('/Accueil/')
        else:
            print('erreur ' + str(user.count()))
    context = {'form': form}
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
        form = ParticipantForm(request.POST or None, instance=user)
        if form.is_valid():
            user.password = hashers.make_password(user.password)
            user.save()

        context = {'user': user,'form': form}
        return render(request, 'sortir/modifierProfil.html', context)

    return redirect('accueil')


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



