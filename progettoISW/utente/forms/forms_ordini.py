from django import forms

from utente.models import Pagamento


class AggiuntaIndirizzo(forms.Form):
    indirizzo_spedizione = forms.CharField(label="Indirizzo di spedizione", max_length=150)


class AggiuntaPagamento(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ["numero_carta", "intestatario", "nome_metodo"]
