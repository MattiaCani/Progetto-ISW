from django import forms
from django.utils.translation import gettext_lazy as _

from utente.models import Prodotto


class NuovoProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "codice_seriale", "tipologia", "descrizione", "prezzo", "disponibilita"]
        labels = {
            "nome": _("Nome"),
            "codice_seriale": _("Codice seriale"),
            "tipologia": _("Tipologia"),
            "descrizione": _("Descrizione"),
            "prezzo": _("Prezzo"),
            "disponibilita": _("Disponibilità"),
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codice_seriale': forms.TextInput(attrs={'class': 'form-control'}),
            'tipologia': forms.TextInput(attrs={'class': 'form-control'}),
            'descrizione': forms.TextInput(attrs={'class': 'form-control'}),
            'prezzo': forms.TextInput(attrs={'class': 'form-control'}),
            'disponibilita': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ModificaProdottoForm(forms.ModelForm):

    class Meta:
        model = Prodotto
        fields = ["nome", "tipologia", "descrizione", "prezzo", "disponibilita"]