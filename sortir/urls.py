from django.conf.urls import url
from django.urls import path
from sortir import views

urlpatterns = [
    path('', views.index),
    path('Accueil/', views.accueil, name='accueil'),
    path('Profil/', views.modifierprofil, name='profil'),
    path('Deconnexion/', views.deconnexion, name='deconnexion'),
    path('Sites/', views.sites, name='sites'),
    path('Villes/', views.villes, name='villes'),
    path('Participants/', views.participants, name='participants'),
    path('GetSession/', views.getsession, name='session'),

    path('CreerSortie/', views.creersortie, name='creersortie'),
    path('AfficherSortie_<idsortie>/', views.affichersortie, name='affichersortie'),
    path('ModifierSortie_<idsortie>/', views.modifiersortie, name='modifiersortie'),

    path('Connexion/', views.connexion, name='connexion'),
    path('AfficherProfil_<idOrganisateur>/', views.afficherprofil, name='afficherprofil'),
    path('AjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
]
