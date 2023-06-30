from django import forms

from utente.models import Prodotto


class NuovoProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "codice_seriale", "tipologia", "descrizione", "prezzo", "disponibilita"]


class ModificaProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "tipologia", "descrizione", "prezzo", "disponibilita"]