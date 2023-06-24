"""
URL configuration for progettoISW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path

import utente.views
import vetrine.views

urlpatterns = [
    path('utente/', include('utente.urls')),
    path('vetrine/', include('vetrine.urls')),
    path('admin/', admin.site.urls),
    path('', utente.views.loginview, name='login'),
    path('logout/', utente.views.logoutview, name='logout'),
    path('vetrinaCliente/', vetrine.views.vetrina_clienteview, name='vetrinaCliente'),
    path('signup/', utente.views.signupview, name='signup'),
    path('vetrinaAmministratore/', vetrine.views.vetrina_amministratoreview, name='vetrinaAmministratore'),
    path('nuovoProdotto/', vetrine.views.nuovo_prodottoview, name='nuovoProdotto'),
    path('rimuovi_prodotto/<str:nomeprodotto>/', vetrine.views.rimuovi_prodotto_view, name='rimuoviProdotto'),
    path('modifica_prodotto/<str:nomeprodotto>/', vetrine.views.modifica_prodotto_view, name='modificaProdotto')
]


