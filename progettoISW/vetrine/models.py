from django.db import models


class ResocontoVendite(models.Model):
    totaleVendite = models.FloatField

    def __init__(self, totaleVendite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totaleVendite = totaleVendite

    def __str__(self):
        return self.totaleVendite


class Vetrina(models.Model):
    ID_vetrina = models.CharField(max_length=30, default="Vetrina", primary_key=True)

    def save(self, *args, **kwargs):
        is_new_instance = self._state.adding
        super().save(*args, **kwargs)
        if is_new_instance:
            VetrinaAmministratore.objects.create(vetrina=self)

    def __str__(self):
        return self.ID_vetrina

    class Meta:
        verbose_name_plural = "Vetrine"


class VetrinaAmministratore(models.Model):
    vetrina = models.OneToOneField(Vetrina, on_delete=models.CASCADE, null=True)
    ID_vetrina_admin = models.CharField(max_length=30, default="Vetrina Amministratore", primary_key=True)

    def __str__(self):
        return self.ID_vetrina_admin

    class Meta:
        verbose_name_plural = "Vetrine Amministratore"
