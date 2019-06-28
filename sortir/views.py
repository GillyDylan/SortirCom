from django.shortcuts import render, redirect
from django.http import HttpResponse
from sortir.forms import ParticipantForm, ConnexionForm
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
    context = {'form': ParticipantForm()}
    return render(request, 'sortir/ajouterParticipant.html', context)



def connection(request):
    form = ConnexionForm(request.POST or None)
    if form.is_valid():
        user = Participant.objects.filter(pseudo=form.cleaned_data['pseudo'])
        if user.count() == 1:
            if hashers.check_password(user.password, form.cleaned_data['password']):
                request.session['userId'] = form.cleaned_data['pseudo']
                return render(request, 'sortir/connecter.html')

    context = {'form': form}
    return render(request, 'sortir/connecter.html', context)


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
    user = Participant()
    form = ParticipantForm(data=(request.POST or None), instance=user)

    print(form.is_valid(), form.errors, type(form.errors))

    if form.is_valid():
        print('je devrais reussir a l\'ajouter en bdd')
        user.password = hashers.make_password(user.password)
        user.save()
        return render(request, 'sortir/index.html')

    context = {'form': form}
    return render(request, 'sortir/ajouterParticipant.html', context)



