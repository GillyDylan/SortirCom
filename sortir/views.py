from django.shortcuts import render, redirect
from django.http import HttpResponse
from sortir.forms import ParticipantForm
from sortir.models import Participant, Sortie, Site
from django.contrib.auth import hashers
# Create your views here.


def workspace(request):
    return HttpResponse("Coucou")


def index(request):
    return render(request, 'sortir/index.html')


def accueil(request):
    return render(request, 'sortir/accueil.html')


def profil(request):
    return render(request, 'sortir/profil.html')


def deconnecter(request):
    return render(request, 'sortir/deconnecter.html')


def formulaireajouterparticipant(request):
    form = ParticipantForm()
    context = {'form': form}
    return render(request, 'sortir/ajouterParticipant.html', context)



def afficherprofil(request, idOrganisateur, idSortie):
    if request.session.__contains__('userId'):
        sortie = Sortie.objects.get(pk=idSortie)
        if (sortie.get(organisateur=idOrganisateur) is not None &
                sortie.participants.get(id=request.session['userId'])) is not None:
            participant = Participant.objects.get(pk=idOrganisateur)
            context = {'participant': participant}
            return render(request, 'sortir/afficherProfil.html', context)

    return render(request,'sortir/index.html')


def modifierprofil(request):
    if request.session.__contains__('userId'):
        user = Participant.objects.get(pk=request.session['userId'])
        form = ParticipantForm()
        if form.is_valid():
            user.pseudo = form.cleaned_data['pseudo'] if user.pseudo != form.cleaned_data['pseudo'] else None
            user.nom = form.cleaned_data['nom'] if user.nom != form.cleaned_data['nom'] else None
            user.prenom = form.cleaned_data['prenom'] if user.prenm != form.cleaned_data['prenom'] else None
            user.password = hashers.make_password(form.cleaned_data['password']) if user.password != hashers.make_password else None
            user.site = form.cleaned_data['site'] if user.site != form.cleaned_data['site'] else None
            user.save()

        context = {'user': user,'form': form}
        return render(request, 'sortir/modifierProfil.html', context)

    return render(request, 'sortir/index.html')


def ajouterparticipant(request):
    # if request.session.__contains__('userId'):
    #    user = Participant.objects.get(pk=request.session['userId'])
    #    if user.administrateur:
    form = ParticipantForm(request.POST or None)

    if form.is_valid():
        newParticipant = Participant()
        newParticipant.pseudo = form.cleaned_data['pseudo']
        newParticipant.nom = form.cleaned_data['nom']
        newParticipant.prenom = form.cleaned_data['prenom']
        newParticipant.password = form.cleaned_data['password']
        newParticipant.email = form.cleaned_data['email']
        newParticipant.telephone = form.cleaned_data['telephone']
        newParticipant.site = form.cleaned_data['site']
        newParticipant.administrateur = form.cleaned_data['administrateur']
        newParticipant.actif = form.cleaned_data['actif']
        newParticipant.save()
        return render(request, 'sortir/index.html')

    context = {'form': form}
    return render(request, 'sortir/ajouterParticipant.html', context)



