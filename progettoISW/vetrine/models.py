from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models import Q  # classe per effettuare query complesse al DB


class ResocontoVendite(models.Model):
    ID_resoconto = models.CharField(max_length=30, default="Resoconto", primary_key=True)

    @property
    def totale_vendite(self):
        return sum(prodotto.guadagno_totale for prodotto in self.prodotto_set.all())

    def __str__(self):
        return self.ID_resoconto

    @staticmethod
    def get_dati_resoconto(request, resoconto_vendite):
        elenco_prodotti = resoconto_vendite.prodotto_set.all()

        elenco_tipologie = elenco_prodotti.values('tipologia').distinct()
        elenco_disponibilita = ['Ultime scorte', 'Disponibile', 'Illimitata']

        disponibilita, tipologia, elenco_prodotti = Vetrina.aggiungi_filtro(request, elenco_prodotti)
        elenco_prodotti = Vetrina.ricerca_prodotto(request, elenco_prodotti)
        elenco_prodotti = Vetrina.azzera_filtri(request, elenco_prodotti)

        tot = sum(prodotto.guadagno_totale for prodotto in elenco_prodotti)

        dati_resoconto = (
            elenco_prodotti,
            elenco_tipologie,
            elenco_disponibilita,
            tipologia,
            disponibilita,
            tot
        )

        return dati_resoconto

    class Meta:
        verbose_name_plural = "Resoconti"


class Vetrina(models.Model):
    ID_vetrina = models.CharField(max_length=30, default="Vetrina", primary_key=True)

    def save(self, *args, **kwargs):
        is_new_instance = self._state.adding
        super().save(*args, **kwargs)
        if is_new_instance:
            VetrinaAmministratore.objects.create(vetrina=self)
            ResocontoVendite.objects.create()

    @staticmethod
    def aggiungi_filtro(request, elenco_prodotti):
        tipologia = request.GET.get('tipologia')
        disponibilita = request.GET.get('disponibilita')
        prezzo_min = request.GET.get('prezzo_min')
        prezzo_max = request.GET.get('prezzo_max')

        nd_i = 0
        nd_f = 0

        if disponibilita == 'Ultime scorte':
            nd_i = 0
            nd_f = 50
        elif disponibilita == 'Disponibile':
            nd_i = 50
            nd_f = 600
        elif disponibilita == 'Illimitata':
            nd_i = 600
            nd_f = 100000000

        if tipologia:
            elenco_prodotti = elenco_prodotti.filter(tipologia=tipologia)
        if disponibilita:
            elenco_prodotti = elenco_prodotti.filter(disponibilita__gte=nd_i, disponibilita__lte=nd_f)
        if prezzo_min:
            elenco_prodotti = elenco_prodotti.filter(prezzo__gte=prezzo_min)  # maggiore o uguale
        if prezzo_max:
            elenco_prodotti = elenco_prodotti.filter(prezzo__lte=prezzo_max)  # minore o uguale

        return disponibilita, tipologia, elenco_prodotti

    @staticmethod
    def ricerca_prodotto(request, elenco_prodotti):
        search_query = request.GET.get('search_query')

        if search_query:
            elenco_prodotti = elenco_prodotti.filter(
                Q(nome__icontains=search_query) | Q(descrizione__icontains=search_query))

        return elenco_prodotti

    @staticmethod
    def azzera_filtri(request, elenco_prodotti):
        reset_filters = request.GET.get('reset_filters')

        if reset_filters:
            elenco_prodotti = get_object_or_404(Vetrina).prodotto_set.all()

        return elenco_prodotti

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


def inizializza_vetrine():
    try:
        vetrina = Vetrina.objects.get(ID_vetrina="Vetrina")
    except ObjectDoesNotExist:
        vetrina = Vetrina.objects.create(ID_vetrina="Vetrina")

    try:
        vetrina_amministratore = VetrinaAmministratore.objects.get(
            ID_vetrina_admin="Vetrina Amministratore")
    except ObjectDoesNotExist:
        vetrina_amministratore = VetrinaAmministratore.objects.create(
            ID_vetrina_admin="Vetrina Amministratore",
            vetrina=vetrina)