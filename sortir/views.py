from django.shortcuts import render
from django.http import HttpResponse
from . import forms
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


def afficherProfil(request, idProfil):
    return render(request,'sortir/index.html')