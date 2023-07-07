import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.shortcuts import render
from utente.forms.auth import LoginForm, SignupForm

from utente.forms.forms_ordini import AggiuntaIndirizzo, AggiuntaPagamento, QuantitaProdotto, QuantitaProdottoVetrina
from utente.models import Utente, Carrello, Prodotto, Ordine, ProdottoCarrello, SessionManager
from vetrine.models import VetrinaAmministratore, Vetrina
from django.core import serializers
import datetime


def logout_view(request):
    SessionManager.logout_manager(request)
    return redirect('login')


def login_view(request):
    form = forms.auth.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.auth.LoginForm(request.POST)
        user = SessionManager.login_manager(request, form)

        if user is not None:
            if user.is_superuser:  # redirect a vetrina diversa a seconda che sia admin o no
                if Utente.objects.filter(username=user.username, is_superuser=True).exists():
                    return redirect('vetrinaAmministratore')
            else:
                return redirect('vetrina')

        else:
            message = 'Login fallito'

    return render(request, 'registration/login.html', {'form': form, 'message': message})


def signup_view(request):
    form = forms.auth.SignupForm()

    if request.method == 'POST':
        form = forms.auth.SignupForm(request.POST)

        flag_valid = SessionManager.signup_manager(form)
        if flag_valid:
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'registration/signup.html', {'form': form})


def carrello(request):
    carrello_utente = get_object_or_404(Carrello, possessore=request.user)

    form_quantita = []

    for item in carrello_utente.lista_prodotti.all():
        form_quantita.append(QuantitaProdotto(initial_value=item.quantita_acquisto))

    carrello_ = zip(carrello_utente.lista_prodotti.all(), form_quantita)
    importo_totale = carrello_utente.importo_totale

    return render(request, "carrello/carrello.html", {"carrello": carrello_, "importo_totale": importo_totale})


def update_quantita(request, codice_seriale):
    if request.method == 'POST':
        form_quantita = QuantitaProdotto(request.POST)

        if form_quantita.is_valid():

            prodotto_carrello, carrello_utente = \
                ProdottoCarrello.update_quantita(form_quantita, request, codice_seriale)

            prodotto_carrello.save()
            carrello_utente.save()

            return redirect('carrello')


def aggiungi_al_carrello(request, codice_seriale):
    if request.method == 'POST':
        form_quantita = QuantitaProdottoVetrina(request.POST)

        carrello_utente, prodotto_carrello = Prodotto.aggiungi_al_carrello(form_quantita, codice_seriale, request)
        if prodotto_carrello is not None and carrello_utente is not None:
            carrello_utente.save()
            prodotto_carrello.save()

        return redirect('vetrina')


def rimuovi_dal_carrello(request, codice_seriale):

    carrello_utente = ProdottoCarrello.rimuovi_dal_carrello(request, codice_seriale)
    carrello_utente.save()

    return redirect('carrello')


def ordine(request):
    if request.method == "POST":
        form_indirizzo = AggiuntaIndirizzo(request.POST)
        form_pagamento = AggiuntaPagamento(request.POST)

        if form_indirizzo.is_valid() and form_pagamento.is_valid():

            nuovo_ordine, carrello_cliente = Ordine.ordina(request, form_indirizzo, form_pagamento)
            nuovo_ordine.save()
            carrello_cliente.save()

            return redirect("vetrina")

    else:
        form_indirizzo = AggiuntaIndirizzo()
        form_pagamento = AggiuntaPagamento()

    return render(request, "carrello/ordine.html", {"form_indirizzo": form_indirizzo, "form_pagamento": form_pagamento})
