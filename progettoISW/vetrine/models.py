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
    vetrinaidadmin = models.CharField(max_length=30, default="", primary_key=True)
    listaProdotti = models.CharField(max_length=2000)

    def __str__(self):
        return self.vetrinaidadmin


class Vetrina(models.Model):
    vetrinaid = models.CharField(max_length=30, default="", primary_key=True)
    listaProdotti = models.CharField(max_length=2000, default="")
    filtro = models.CharField(max_length=20, choices=Filtro.choices, default=Filtro.NO_FILTRO)
    vetrina = models.OneToOneField(VetrinaAmministratore, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.vetrinaid

    def set_listaprodotti(self, prodlist):
        self.listaProdotti = json.dumps(prodlist)

    def get_listaprodotti(self):
        return json.loads(self.listaProdotti)


