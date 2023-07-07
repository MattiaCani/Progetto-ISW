import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.shortcuts import render
from utente.forms.auth import LoginForm, SignupForm
from utente.forms.forms_ordini import AggiuntaIndirizzo, AggiuntaPagamento, QuantitaProdotto, QuantitaProdottoVetrina, \
    Pagamento
from utente.models import Utente, Carrello, Prodotto, Ordine, ProdottoCarrello
from vetrine.models import VetrinaAmministratore, Vetrina
from django.core import serializers
import datetime


def logout_view(request):
    logout(request)
    return redirect('login')


def inizializza_vetrine():
    try:
        Vetrina.objects.get(ID_vetrina="Vetrina")
    except ObjectDoesNotExist:
        Vetrina.objects.create(ID_vetrina="Vetrina")


def login_view(request):
    form = forms.auth.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.auth.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)

                inizializza_vetrine()

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

        if form.is_valid():
            form.save()

            inizializza_vetrine()

            # login(request, authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1']))

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
            quantita_acquisto = form_quantita.cleaned_data['quantita_acquisto']

            carrello_utente = get_object_or_404(Carrello, possessore=request.user)
            prodotto_carrello = carrello_utente.lista_prodotti.get(prodotto_id=codice_seriale)

            carrello_utente.importo_totale -= prodotto_carrello.prodotto.prezzo * prodotto_carrello.quantita_acquisto

            prodotto_carrello.quantita_acquisto = quantita_acquisto
            prodotto_carrello.save()

            carrello_utente.importo_totale += prodotto_carrello.prodotto.prezzo * float(quantita_acquisto)
            carrello_utente.save()

            return redirect('carrello')


def aggiungi_al_carrello(request, codice_seriale):
    if request.method == 'POST':
        form_quantita = QuantitaProdottoVetrina(request.POST)

        if form_quantita.is_valid():
            quantita_acquisto = form_quantita.cleaned_data['quantita_acquisto']

            prodotto = get_object_or_404(Prodotto, pk=codice_seriale)
            carrello_utente = get_object_or_404(Carrello, possessore=request.user)

            try:
                carrello_utente.lista_prodotti.get(utente=request.user, prodotto=prodotto)
            except ProdottoCarrello.DoesNotExist:
                prodotto_carrello = ProdottoCarrello.objects.create(utente=request.user, prodotto=prodotto,
                                                                    quantita_acquisto=float(quantita_acquisto))

                carrello_utente.lista_prodotti.add(prodotto_carrello)

                carrello_utente.importo_totale += prodotto.prezzo * float(quantita_acquisto)

                carrello_utente.save()
                prodotto_carrello.save()

            return redirect('vetrina')


def rimuovi_dal_carrello(request, codice_seriale):
    prodotto = get_object_or_404(Prodotto, pk=codice_seriale)
    carrello_utente = get_object_or_404(Carrello, possessore=request.user)
    prodotto_carrello = carrello_utente.lista_prodotti.get(utente=request.user, prodotto=prodotto)

    carrello_utente.importo_totale -= prodotto_carrello.prodotto.prezzo * prodotto_carrello.quantita_acquisto

    get_object_or_404(ProdottoCarrello, utente=request.user, prodotto=prodotto).delete()

    carrello_utente.save()

    return redirect('carrello')


def ordine(request):
    if request.method == "POST":
        form_indirizzo = AggiuntaIndirizzo(request.POST)
        form_pagamento = AggiuntaPagamento(request.POST)

        if form_indirizzo.is_valid() and form_pagamento.is_valid():
            indirizzo = form_indirizzo.cleaned_data['indirizzo_spedizione']

            numero_carta = form_pagamento.cleaned_data['numero_carta']
            intestatario = form_pagamento.cleaned_data['intestatario']
            nome_metodo = form_pagamento.cleaned_data['nome_metodo']

            cliente = get_object_or_404(Utente, username=request.user)
            carrello_cliente = get_object_or_404(Carrello, possessore=request.user)

            dati_carrello = {}

            for prodotto in carrello_cliente.lista_prodotti.all():
                prodotto.prodotto.pezzi_venduti += prodotto.quantita_acquisto
                prodotto.prodotto.disponibilita -= prodotto.quantita_acquisto
                prodotto.prodotto.save()

                dati_carrello[str(prodotto.prodotto.nome)] = prodotto.quantita_acquisto

            json_carrello = json.dumps(dati_carrello)

            nuovo_ordine = Ordine.objects.create(
                cliente=cliente,
                carrello=json_carrello,
                email_cliente=cliente.email,
                nome_cliente=cliente.first_name,
                numero_ordine=hash(carrello_cliente.lista_prodotti),
                data_ordine=datetime.datetime.now(),
                indirizzo_spedizione=indirizzo,
                numero_carta=numero_carta,
                intestatario=intestatario,
                nome_metodo=nome_metodo
            )

            nuovo_ordine.save()

            carrello_cliente.importo_totale = 0
            carrello_cliente.lista_prodotti.all().delete()
            carrello_cliente.save()

            return redirect("vetrina")

    else:
        form_indirizzo = AggiuntaIndirizzo()
        form_pagamento = AggiuntaPagamento()

    return render(request, "carrello/ordine.html", {"form_indirizzo": form_indirizzo, "form_pagamento": form_pagamento})
