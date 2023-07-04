from django.db import models
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


class Prodotto(models.Model):
    pezzi_venduti = models.PositiveIntegerField(default=0)
    disponibilita = models.PositiveIntegerField(default=100)

    nome = models.CharField(max_length=30, unique=True)
    codice_seriale = models.IntegerField(unique=True, default=0, primary_key=True)
    tipologia = models.CharField(max_length=30)
    descrizione = models.TextField(default="")
    prezzo = models.FloatField(default=0.0)

    vetrina = models.ForeignKey(Vetrina, on_delete=models.PROTECT, null=True, default="Vetrina")
    resVendite = models.ForeignKey(ResocontoVendite, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.codice_seriale)

    class Meta:
        verbose_name_plural = "Prodotti"


class ProdottoCarrello(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, null=True)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, null=True)
    quantita_acquisto = models.IntegerField(default=1)

    def __str__(self):
        return str(self.prodotto)


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
    carrello = models.OneToOneField(Carrello, on_delete=models.CASCADE, null=True)
    email_cliente = models.EmailField(max_length=30)
    nome_cliente = models.CharField(max_length=30)
    numero_ordine = models.PositiveIntegerField(unique=True, primary_key=True)
    data_ordine = models.DateTimeField
    indirizzo_spedizione = models.CharField(max_length=50)
    info_pagamento = Pagamento(numero_carta=models.BigIntegerField,
                               intestatario=models.CharField(max_length=50),
                               nome_metodo=models.CharField(max_length=20, choices=MetodoPagamento.choices,
                                                           default=MetodoPagamento.CREDITO))

    def __str__(self):
        return str(self.numero_ordine)

    class Meta:
        verbose_name_plural = "Ordini"
