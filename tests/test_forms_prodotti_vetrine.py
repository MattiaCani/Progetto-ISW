import unittest
from django.test import TestCase
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm
from utente.models import Prodotto

class FormsProdottiTestCase(TestCase):
    def test_nuovo_prodotto_form_valid_data(self):
        form = NuovoProdottoForm(data={
            'nome': 'Prodotto 1',
            'codice_seriale': '12345',
            'tipologia': 'Tipo A',
            'descrizione': 'Descrizione del prodotto 1',
            'prezzo': 10.99,
            'disponibilita': True
        })
        self.assertTrue(form.is_valid())

    def test_nuovo_prodotto_form_invalid_data(self):
        form = NuovoProdottoForm(data={
            'nome': '',
            'codice_seriale': '12345',
            'tipologia': 'Tipo A',
            'descrizione': 'Descrizione del prodotto 1',
            'prezzo': -10.99,
            'disponibilita': True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Verifica che ci siano 2 errori

    def test_modifica_prodotto_form_valid_data(self):
        prodotto = Prodotto.objects.create(
            nome='Prodotto 1',
            codice_seriale='12345',
            tipologia='Tipo A',
            descrizione='Descrizione del prodotto 1',
            prezzo=10.99,
            disponibilita=True
        )
        form = ModificaProdottoForm(data={
            'nome': 'Prodotto modificato',
            'tipologia': 'Tipo B',
            'descrizione': 'Descrizione del prodotto modificato',
            'prezzo': 15.99,
            'disponibilita': False
        }, instance=prodotto)
        self.assertTrue(form.is_valid())

    def test_modifica_prodotto_form_invalid_data(self):
        prodotto = Prodotto.objects.create(
            nome='Prodotto 1',
            codice_seriale='12345',
            tipologia='Tipo A',
            descrizione='Descrizione del prodotto 1',
            prezzo=10.99,
            disponibilita=True
        )
        form = ModificaProdottoForm(data={
            'nome': '',
            'tipologia': 'Tipo B',
            'descrizione': 'Descrizione del prodotto modificato',
            'prezzo': -15.99,
            'disponibilita': False
        }, instance=prodotto)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Verifica che ci siano 2 errori

if __name__ == '__main__':
    unittest.main()
