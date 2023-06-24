from django import forms

class modificaProdottoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    codiceSeriale = forms.IntegerField()
    tipologia = forms.CharField(max_length=100)
    descrizione = forms.CharField(widget=forms.Textarea)
    prezzo = forms.FloatField()
    disponibilita = forms.IntegerField()
