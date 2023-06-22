from django.db import models
from utente.enums import Filtro
import json

# Create your models here.


class ResocontoVendite(models.Model):
    totaleVendite = models.FloatField

    def __init__(self, totaleVendite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totaleVendite = totaleVendite

    def __str__(self):
        return self.totaleVendite


class VetrinaAmministratore(models.Model):
    listaProdotti = models.CharField(max_length=2000)

    def __init__(self, listaProdotti, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listaProdotti = listaProdotti

    def __str__(self):
        return self.listaProdotti




class Vetrina(models.Model):
    listaProdotti = models.CharField(max_length=2000)
    filtro = models.CharField(max_length=20, choices=Filtro.choices, default=Filtro.NO_FILTRO)
    vetrina = models.OneToOneField(VetrinaAmministratore, on_delete=models.CASCADE, null=True)

    def __init__(self, listaProdotti, filtro=Filtro.NO_FILTRO, vetrina=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listaProdotti = listaProdotti
        self.filtro = filtro
        self.vetrina = vetrina

    def __str__(self):
        return self.listaProdotti

    def set_listaprodotti(self, prodlist):
        self.listaProdotti = json.dumps(prodlist)

    def get_listaprodotti(self):
        return json.loads(self.listaProdotti)


class Prodotto(models.Model):
    pezziVenduti = models.PositiveIntegerField
    disponibilita = models.PositiveIntegerField
    nome = models.CharField(max_length=30)
    codiceSeriale = models.AutoField  # unique
    tipologia = models.CharField(max_length=30)
    descrizione = models.TextField
    quantitaAcquisto = models.PositiveIntegerField(default=1)
    prezzo = models.FloatField
    vetrina = models.ForeignKey(Vetrina, on_delete=models.PROTECT, null=True)
    vetrinaAmministratore = models.ForeignKey(VetrinaAmministratore, on_delete=models.CASCADE, null=True)
    resVendite = models.ForeignKey(ResocontoVendite, on_delete=models.PROTECT, null=True)

    def __init__(self, pezziVenduti, disponibilita, nome, tipologia, descrizione, quantitaAcquisto=1, prezzo=0.0,
                 vetrina=None, vetrinaAmministratore=None, resVendite=None, *args, **kwargs):
        super(Prodotto, self).__init__(*args, **kwargs)
        self.pezziVenduti = pezziVenduti
        self.disponibilita = disponibilita
        self.nome = nome
        self.tipologia = tipologia
        self.descrizione = descrizione
        self.quantitaAcquisto = quantitaAcquisto
        self.prezzo = prezzo
        self.vetrina = vetrina
        self.vetrinaAmministratore = vetrinaAmministratore
        self.resVendite = resVendite

    def __str__(self):
        return self.codiceSeriale
