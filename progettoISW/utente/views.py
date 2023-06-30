from django.conf import settings

from . import forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.shortcuts import render
from utente.forms.auth import LoginForm, SignupForm
from utente.forms.forms_ordini import AggiuntaIndirizzo, AggiuntaPagamento
from utente.models import Utente, Carrello, Prodotto, Ordine, ProdottoCarrello
import datetime


def logout_view(request):
    logout(request)
    return redirect('login')


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

            # login(request, authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1']))

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'registration/signup.html', {'form': form})


def carrello(request):
    carrello_utente = get_object_or_404(Carrello, possessore=request.user)

    form_quantita = request.POST.get('quantita_acquisto')

    # Gestione della quantita da fare

    return render(request, "carrello/carrello.html", {"carrello": carrello_utente, "form": form_quantita})


def aggiungi_al_carrello(request, codice_seriale, quantita_acquisto):
    prodotto = get_object_or_404(Prodotto, pk=codice_seriale)
    prodotto_carrello = ProdottoCarrello.objects.create(utente=request.user, prodotto=prodotto, quantita_acquisto=quantita_acquisto)

    carrello_utente = get_object_or_404(Carrello, possessore=request.user)
    carrello_utente.lista_prodotti.add(prodotto_carrello)

    carrello_utente.importo_totale += prodotto.prezzo * quantita_acquisto

    carrello_utente.save()
    prodotto_carrello.save()

    return redirect('vetrina')


def rimuovi_dal_carrello(request, codice_seriale):
    prodotto = get_object_or_404(Prodotto, pk=codice_seriale)
    carrello_utente = get_object_or_404(Carrello, possessore=request.user)
    prodotto_carrello = carrello_utente.lista_prodotti.get(utente=request.user, prodotto=prodotto)

    carrello_utente.importo_totale -= prodotto_carrello.prodotto.prezzo * prodotto_carrello.quantita_acquisto

    get_object_or_404(ProdottoCarrello, utente=request.user, prodotto=prodotto).delete()

    return redirect('carrello')


def ordine(request):
    if request.method == "POST":
        form_indirizzo = AggiuntaIndirizzo(request.POST)
        form_pagamento = AggiuntaPagamento(request.POST)

        if form_indirizzo.is_valid() and form_pagamento.is_valid():
            indirizzo = form_indirizzo.cleaned_data
            pagamento = form_pagamento.cleaned_data

            cliente = get_object_or_404(Utente, username=request.user)
            carrello_cliente = get_object_or_404(Carrello, possessore=request.user)

            nuovo_ordine = Ordine.objects.create(
                cliente=cliente,
                carrello=carrello_cliente,
                email_cliente=cliente.email,
                nome_cliente=cliente.first_name,
                numero_ordine=hash(carrello_cliente.lista_prodotti),
                # data_ordine=datetime.datetime.now(), non funziona
                # indirizzo_spedizione=indirizzo, non funziona
                # info_pagamento=pagamento non funziona
            )

            nuovo_ordine.save()

            return redirect("vetrina")

    else:
        form_indirizzo = AggiuntaIndirizzo()
        form_pagamento = AggiuntaPagamento()

    return render(request, "carrello/ordine.html", {"form_indirizzo": form_indirizzo, "form_pagamento": form_pagamento})