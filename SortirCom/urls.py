"""SortirCom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from sortir import views

urlpatterns = [
    path('', include('sortir.urls')),
    path('Ajax/', include('sortir.urls')),
    path('Accueil', views.index),
    path('Profil', views.index),
    path('Participants', views.index),
    path('Sites', views.index),
    path('Villes', views.index),

    path('CreerSortie', views.index),
    path('AfficherSortie_<int:idsortie>', views.index),
    path('ModifierSortie_<int:idsortie>', views.index),
    path('AnnulerSortie_<int:idsortie>', views.index),

    path('AfficherProfil_<int:idOrganisateur>', views.index),
    path('ModifierProfil', views.index),
    path('Connexion', views.index),
    path('Deconnexion', views.index),
    path('AjouterParticipant', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
