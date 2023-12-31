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

    path('', utente.views.login_view, name='login'),
    path('logout/', utente.views.logout_view, name='logout'),
    path('signup/', utente.views.signup_view, name='signup'),

    path('carrello/', utente.views.carrello, name='carrello'),
    path('ordine/', utente.views.ordine, name='ordine'),
    path('rimuovi_dal_carrello/<int:codice_seriale>/', utente.views.rimuovi_dal_carrello, name='rimuovi_dal_carrello'),
    path('aggiungi_al_carrello/<int:codice_seriale>/', utente.views.aggiungi_al_carrello, name='aggiungi_al_carrello'),
    path('update_quantita/<int:codice_seriale>/', utente.views.update_quantita, name='update_quantita'),

    path('vetrina/', vetrine.views.vetrina_cliente_view, name='vetrina'),
    path('vetrina_amministratore/', vetrine.views.vetrina_amministratore_view, name='vetrina_amministratore'),

    path('nuovo_prodotto/', vetrine.views.nuovo_prodotto_view, name='nuovo_prodotto'),
    path('rimuovi_prodotto/<int:codice_seriale>/', vetrine.views.rimuovi_prodotto_view, name='rimuovi_prodotto'),
    path('modifica_prodotto/<int:codice_seriale>/', vetrine.views.modifica_prodotto_view, name='modifica_prodotto'),

    path('vetrina_amministratore/resoconto_vendite/', vetrine.views.resoconto_vendite_view, name='resoconto_vendite'),
    path('vetrina_amministratore/resoconto_vendite/dettaglio_ordine/<int:numero_ordine>/',
         vetrine.views.dettaglio_ordine_view, name='dettaglio_ordine')
]

