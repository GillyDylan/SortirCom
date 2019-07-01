from django.conf.urls import url
from django.urls import path
from sortir import views

urlpatterns = [
    path('', views.index),
    path('Accueil/', views.accueil, name='accueil'),
    path('Profil/', views.modifierprofil, name='profil'),
    path('Deconnexion/', views.deconnexion, name='deconnexion'),
    path('Connexion/', views.connexion, name='connexion'),
    path('AfficherProfil/<idOrganisateur>/', views.afficherprofil, name='afficherprofil'),
    path('FormulaireAjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
    path('AjouterParticipant/', views.ajouterparticipant, name='ajouterparticipant'),
]
