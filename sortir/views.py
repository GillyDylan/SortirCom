from django.shortcuts import render
from django.http import  HttpResponse
from . import forms
# Create your views here.


def workspace(request):
    return HttpResponse("Coucou")


def index(request):
    return HttpResponse("Index")


def test(request):
    return HttpResponse("ajax")
