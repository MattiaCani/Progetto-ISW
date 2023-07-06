import unittest
from django.test import TestCase
from utente.forms.forms_ordini import AggiuntaIndirizzo, AggiuntaPagamento, QuantitaProdotto
from utente.models import Pagamento

class FormsOrdiniTestCase(TestCase):
    def test_aggiunta_indirizzo_form_valid_data(self):
        form = AggiuntaIndirizzo(data={
            'indirizzo_spedizione': 'Via Roma 123'
        })
        self.assertTrue(form.is_valid())

    def test_aggiunta_indirizzo_form_invalid_data(self):
        form = AggiuntaIndirizzo(data={
            'indirizzo_spedizione': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Verifica che ci sia 1 errore

    def test_aggiunta_pagamento_form_valid_data(self):
        form = AggiuntaPagamento(data={
            'numero_carta': '1234567890',
            'intestatario': 'Mario Rossi',
            'nome_metodo': 'Carta di credito'
        })
        self.assertTrue(form.is_valid())

    def test_aggiunta_pagamento_form_invalid_data(self):
        form = AggiuntaPagamento(data={
            'numero_carta': '1234',
            'intestatario': '',
            'nome_metodo': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Verifica che ci siano 2 errori (nome_metodo non è mai errore)

    def test_quantita_prodotto_form_valid_data(self):
        form = QuantitaProdotto(data={
            'quantita_acquisto': '5'
        })
        self.assertTrue(form.is_valid())

    def test_quantita_prodotto_form_invalid_data(self):
        form = QuantitaProdotto(data={
            'quantita_acquisto': '0'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Verifica che ci sia 1 errore

if __name__ == '__main__':
    unittest.main()
