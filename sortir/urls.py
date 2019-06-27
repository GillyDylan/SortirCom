from django.conf.urls import url
from django.urls import path
from sortir import views

urlpatterns = [
    path('coco/', views.workspace)
]