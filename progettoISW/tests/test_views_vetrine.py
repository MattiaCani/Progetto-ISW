import unittest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from vetrine.models import Vetrina, VetrinaAmministratore, Prodotto
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm

class VetrineViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.vetrina = Vetrina.objects.create()
        self.vetrina_amministratore = VetrinaAmministratore.objects.create(vetrina=self.vetrina)
        self.prodotto = Prodotto.objects.create(
            nome='Prodotto 1',
            tipologia='Tipo 1',
            descrizione='Descrizione del prodotto 1',
            prezzo=10.0,
            disponibilita=True
        )

    def test_vetrina_cliente_view(self):
        response = self.client.get(reverse('vetrina_cliente'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vetrina')

    def test_vetrina_amministratore_view(self):
        response = self.client.get(reverse('vetrina_amministratore'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vetrina Amministratore')

    def test_nuovo_prodotto_view(self):
        response = self.client.get(reverse('nuovo_prodotto'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('nuovo_prodotto'), {
            'nome': 'Nuovo prodotto',
            'tipologia': 'Tipo 2',
            'descrizione': 'Descrizione del nuovo prodotto',
            'prezzo': 20.0,
            'disponibilita': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina_amministratore'))

        nuovo_prodotto = Prodotto.objects.filter(nome='Nuovo prodotto').first()
        self.assertIsNotNone(nuovo_prodotto)

    def test_rimuovi_prodotto_view(self):
        response = self.client.get(reverse('rimuovi_prodotto', args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina_amministratore'))

        prodotto = Prodotto.objects.filter(codice_seriale=self.prodotto.codice_seriale).first()
        self.assertIsNone(prodotto)

    def test_modifica_prodotto_view(self):
        response = self.client.get(reverse('modifica_prodotto', args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('modifica_prodotto', args=[self.prodotto.codice_seriale]), {
            'nome': 'Prodotto modificato',
            'tipologia': 'Tipo modificato',
            'descrizione': 'Descrizione del prodotto modificato',
            'prezzo': 15.0,
            'disponibilita': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina_amministratore'))

        prodotto_modificato = Prodotto.objects.filter(nome='Prodotto modificato').first()
        self.assertIsNotNone(prodotto_modificato)
        self.assertEqual(prodotto_modificato.tipologia, 'Tipo modificato')
        self.assertEqual(prodotto_modificato.prezzo, 15.0)
        self.assertFalse(prodotto_modificato.disponibilita)

if __name__ == '__main__':
    unittest.main()
