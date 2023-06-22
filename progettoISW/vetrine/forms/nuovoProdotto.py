from django import forms


class nuovoProdottoForm(forms.Form):
    nome = forms.CharField(max_length=63)
    codiceSeriale = forms.IntegerField()
    tipologia = forms.CharField(max_length=100, required=False)
    descrizione = forms.CharField(max_length=500, required=False)
    prezzo = forms.FloatField()
    disponibilita = forms.IntegerField()


