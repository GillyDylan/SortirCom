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
    path('GetSorties/', views.getsorties, name='sorties'),
    path('GetLieux/', views.getlieux, name='lieux'),

    path('AfficherSortie_<int:idsortie>/', views.affichersortie, name='affichersortie'),
    path('Inscription_<int:idsortie>/', views.inscription, name='inscription'),


    path('ModifierSortie_<int:idsortie>/', views.modifiersortie, name='modifiersortie'),
    path('AnnulerSortie_<int:idsortie>/', views.annulersortie, name='annulersortie'),

    path('Connexion/', views.connexion, name='connexion'),
    path('AfficherProfil_<int:idOrganisateur>/', views.afficherprofil, name='afficherprofil'),
    path('AjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
    path('CreerSortie/', views.creersortie, name='creersortie'),

    path('ModifierProfil/', views.modifierprofil, name='modifierprofil')
]
