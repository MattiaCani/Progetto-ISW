from django.db import models


class Filtro(models.TextChoices):
    NO_FILTRO = 'NoFiltro'
    PER_TIPOLOGIA = 'PerTipologia'
    PER_PREZZO = 'PerPrezzo'
    PER_NVENDITE = 'PerNumeroVendite'
    PER_DISPONIBILITA = 'PerDisponibilità'


class MetodoPagamento(models.TextChoices):
    CREDITO = 'Carta di credito'
    DEBITO = 'Carta di debito'
