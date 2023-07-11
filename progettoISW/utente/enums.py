from django.db import models


class MetodoPagamento(models.TextChoices):
    CREDITO = 'Carta di credito'
    DEBITO = 'Carta di debito'
