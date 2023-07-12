import unittest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from vetrine.models import Vetrina, VetrinaAmministratore
from utente.models import Utente, Prodotto, inizializza_vetrine
from vetrine.views import vetrina_cliente_view, vetrina_amministratore_view
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Utente.objects.create(username='testuser', email='test@example.com')
        self.vetrina, _ = Vetrina.objects.get_or_create(ID_vetrina='Test Vetrina')
        self.prodotto = Prodotto.objects.create(
            nome='Test Prodotto',
            codice_seriale=1,
            tipologia='Test Tipologia',
            descrizione='Test Descrizione',
            prezzo=10.0,
            vetrina= self.vetrina
        )

    def test_vetrina_cliente_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.get(reverse('vetrina'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Prodotto')

    def test_vetrina_amministratore_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.get(reverse('vetrina_amministratore'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Prodotto')

    def test_nuovo_prodotto_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.post(reverse('nuovo_prodotto'), {
            'nome': 'Nuovo Prodotto',
            'codice_seriale': 2,
            'tipologia': 'Nuova Tipologia',
            'descrizione': 'Nuova Descrizione',
            'prezzo': 20.0,
            'vetrina': self.vetrina
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prodotto.objects.count(), 2)

    def test_rimuovi_prodotto_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.get(reverse('rimuovi_prodotto', args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prodotto.objects.count(), 0)

    def test_modifica_prodotto_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.post(reverse('modifica_prodotto', args=[self.prodotto.codice_seriale]), {
            'nome': 'Modifica Prodotto',
            'codice_seriale': self.prodotto.codice_seriale,
            'tipologia': 'Modifica Tipologia',
            'descrizione': 'Modifica Descrizione',
            'prezzo': 30.0,
            'vetrina': self.vetrina
        })
        self.assertEqual(response.status_code, 302)
        self.prodotto.refresh_from_db()
        self.assertEqual(self.prodotto.nome, 'Modifica Prodotto')
        self.assertEqual(self.prodotto.prezzo, 30.0)

    def test_resoconto_vendite_view(self):
        self.client.login(username='testuser', email='test@example.com')
        response = self.client.get(reverse('resoconto_vendite'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Prodotto')

    def test_dettaglio_ordine_view(self):
        ordine = self.user.ordine_set.create(numero_ordine=1, data_ordine='2021-01-01', numero_carta=1234567890)
        response = self.client.get(reverse('dettaglio_ordine',  args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
