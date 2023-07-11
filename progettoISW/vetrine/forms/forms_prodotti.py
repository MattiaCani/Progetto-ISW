from django import forms
from django.utils.translation import gettext_lazy as _

from utente.models import Prodotto


class NuovoProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "codice_seriale", "tipologia", "descrizione", "prezzo", "disponibilita"]
        labels = {
            "disponibilita": _("Disponibilità"),
        }
        widgets = {
            'descrizione': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ModificaProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "tipologia", "descrizione", "prezzo", "disponibilita"]