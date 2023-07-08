from json2html import json2html
from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.shortcuts import get_object_or_404
import json
import datetime
from vetrine.models import inizializza_vetrine, ResocontoVendite
from utente.enums import MetodoPagamento
from django.contrib.auth.models import AbstractUser

from vetrine.models import VetrinaAmministratore, Vetrina, ResocontoVendite


class Utente(AbstractUser):
    email = models.EmailField(max_length=30, unique=True)

    def save(self, *args, **kwargs):
        is_new_instance = self._state.adding
        super().save(*args, **kwargs)
        if is_new_instance and not self.is_superuser:
            Carrello.objects.create(possessore=self)

    class Meta:
        verbose_name_plural = "Utenti"


class SessionManager(models.Model):

    @staticmethod
    def login_manager(request, form):
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                inizializza_vetrine()
            return user

    @staticmethod
    def logout_manager(request):
        logout(request)

    @staticmethod
    def signup_manager(form):
        if form.is_valid():
            form.save()
            inizializza_vetrine()

        return form.is_valid()


class Prodotto(models.Model):
    pezzi_venduti = models.PositiveIntegerField(default=0)
    disponibilita = models.PositiveIntegerField(default=100)

    nome = models.CharField(max_length=30, unique=True)
    codice_seriale = models.IntegerField(unique=True, default=0, primary_key=True)
    tipologia = models.CharField(max_length=30)
    descrizione = models.TextField(default="")
    prezzo = models.FloatField(default=0.0)

    vetrina = models.ForeignKey(Vetrina, on_delete=models.PROTECT, null=True, default="Vetrina")
    resoconto_vendite = models.ForeignKey(ResocontoVendite, on_delete=models.PROTECT, null=True, default="Resoconto")

    @property
    def guadagno_totale(self):
        return self.pezzi_venduti * self.prezzo

    def __str__(self):
        return str(self.codice_seriale)

    @staticmethod
    def aggiungi_al_carrello(form_quantita, codice_seriale, request):
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

                return carrello_utente, prodotto_carrello
        return None, None

    class Meta:
        verbose_name_plural = "Prodotti"


class ProdottoCarrello(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, null=True)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, null=True)
    quantita_acquisto = models.IntegerField(default=1)

    def __str__(self):
        return str(self.prodotto)

    @staticmethod
    def update_quantita(form_quantita, request, codice_seriale):
        quantita_acquisto = form_quantita.cleaned_data['quantita_acquisto']

        carrello_utente = get_object_or_404(Carrello, possessore=request.user)
        prodotto_carrello = carrello_utente.lista_prodotti.get(prodotto_id=codice_seriale)

        carrello_utente.importo_totale -= prodotto_carrello.prodotto.prezzo * prodotto_carrello.quantita_acquisto

        prodotto_carrello.quantita_acquisto = quantita_acquisto
        carrello_utente.importo_totale += prodotto_carrello.prodotto.prezzo * float(quantita_acquisto)

        return prodotto_carrello, carrello_utente

    @staticmethod
    def rimuovi_dal_carrello(request, codice_seriale):
        prodotto = get_object_or_404(Prodotto, pk=codice_seriale)
        carrello_utente = get_object_or_404(Carrello, possessore=request.user)
        prodotto_carrello = carrello_utente.lista_prodotti.get(utente=request.user, prodotto=prodotto)

        carrello_utente.importo_totale -= prodotto_carrello.prodotto.prezzo * prodotto_carrello.quantita_acquisto

        get_object_or_404(ProdottoCarrello, utente=request.user, prodotto=prodotto).delete()

        return carrello_utente

    class Meta:
        verbose_name_plural = "Prodotti Carrello"


class Carrello(models.Model):
    possessore = models.OneToOneField(Utente, on_delete=models.CASCADE, null=True)
    lista_prodotti = models.ManyToManyField('utente.ProdottoCarrello', blank=True)
    importo_totale = models.FloatField(default=0.0)

    def __str__(self):
        return self.possessore.username

    class Meta:
        verbose_name_plural = "Carrelli"


class Pagamento(models.Model):
    numero_carta = models.PositiveBigIntegerField(default=1)
    intestatario = models.CharField(max_length=50, default="")
    nome_metodo = models.CharField(max_length=20, choices=MetodoPagamento.choices, default=MetodoPagamento.CREDITO)

    def __str__(self):
        return self.numero_carta

    class Meta:
        verbose_name_plural = "Pagamenti"


class Ordine(models.Model):
    cliente = models.ForeignKey(Utente, on_delete=models.CASCADE, null=True)
    carrello = models.JSONField()

    numero_ordine = models.PositiveBigIntegerField(unique=True, primary_key=True)
    data_ordine = models.DateTimeField("data ordine")

    indirizzo_spedizione = models.CharField(max_length=50)

    numero_carta = models.PositiveBigIntegerField()
    intestatario = models.CharField(max_length=50)
    nome_metodo = models.CharField(max_length=20, choices=MetodoPagamento.choices, default=MetodoPagamento.CREDITO)

    @property
    def importo_totale(self):
        acquisti = json.loads(self.carrello)

        return sum(item['Prezzo'] * item['Quantita'] for item in acquisti)

    @property
    def stampa_acquisti(self):
        acquisti = json.loads(self.carrello)

        data = []

        for item in acquisti:
            data.append({
                "Prodotto": item["Prodotto"],
                "Prezzo": item["Prezzo"],
                "Quantita": item["Quantita"]
            })

        return json2html.convert(json=data)

    def __str__(self):
        return str(self.numero_ordine)

    @staticmethod
    def ordina(request, form_indirizzo, form_pagamento):
        indirizzo = form_indirizzo.cleaned_data['indirizzo_spedizione']

        numero_carta = form_pagamento.cleaned_data['numero_carta']
        intestatario = form_pagamento.cleaned_data['intestatario']
        nome_metodo = form_pagamento.cleaned_data['nome_metodo']

        cliente = get_object_or_404(Utente, username=request.user)
        carrello_cliente = get_object_or_404(Carrello, possessore=request.user)

        list_carrello = []

        for prodotto in carrello_cliente.lista_prodotti.all():
            prodotto.prodotto.pezzi_venduti += prodotto.quantita_acquisto
            prodotto.prodotto.disponibilita -= prodotto.quantita_acquisto
            prodotto.prodotto.save()

            dati_carrello = {"Prodotto": str(prodotto.prodotto.nome),
                             "Prezzo": prodotto.prodotto.prezzo,
                             "Quantita": prodotto.quantita_acquisto}

            list_carrello.append(dati_carrello)

        json_carrello = json.dumps(list_carrello)

        nuovo_ordine = Ordine.objects.create(
            cliente=cliente,
            carrello=json_carrello,
            numero_ordine=hash(carrello_cliente.lista_prodotti),
            data_ordine=datetime.datetime.now(),
            indirizzo_spedizione=indirizzo,
            numero_carta=numero_carta,
            intestatario=intestatario,
            nome_metodo=nome_metodo
        )

        carrello_cliente.importo_totale = 0
        carrello_cliente.lista_prodotti.all().delete()

        return nuovo_ordine, carrello_cliente

    class Meta:
        verbose_name_plural = "Ordini"
