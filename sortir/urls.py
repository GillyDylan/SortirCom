from django.conf.urls import url
from django.urls import path
from sortir import views

urlpatterns = [
    path('coco', views.workspace),
    path('', views.index),
    path('Accueil/', views.accueil),
    path('Profil/', views.profil),
    path('Deconnecter/', views.deconnecter),
    path('FormulaireAjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
    path('AjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
]
