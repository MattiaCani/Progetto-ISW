from django import forms

from utente.models import Pagamento


class AggiuntaIndirizzo(forms.Form):
    indirizzo_spedizione = forms.CharField(label="Indirizzo di spedizione", max_length=150)


class AggiuntaPagamento(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ["numero_carta", "intestatario", "nome_metodo"]


class QuantitaProdotto(forms.Form):
    quantita_acquisto = forms.ChoiceField(label="", choices=[(str(i), str(i)) for i in range(1, 11)],
                                          widget=forms.Select(attrs={'onchange': 'this.form.submit()'}))

    def __init__(self, *args, **kwargs):
        initial_value = kwargs.pop('initial_value', None)
        super().__init__(*args, **kwargs)
        if initial_value is not None:
            self.fields['quantita_acquisto'].initial = initial_value


class QuantitaProdottoVetrina(forms.Form):
    quantita_acquisto = forms.ChoiceField(label="", choices=[(str(i), str(i)) for i in range(1, 11)])

