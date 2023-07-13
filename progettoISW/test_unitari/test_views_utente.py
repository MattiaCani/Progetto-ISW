import unittest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from utente.models import Utente, Carrello, Prodotto, ProdottoCarrello

class UtenteViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.utente = Utente.objects.create(username='testuser', email='test@example.com')
        self.carrello = Carrello.objects.create(possessore=self.utente)
        self.prodotto = Prodotto.objects.create(nome='Prodotto 1', codice_seriale=1, prezzo=10.0)
        self.prodotto_carrello = ProdottoCarrello.objects.create(utente=self.utente, prodotto=self.prodotto, quantita_acquisto=2)
        self.client.login(username='testuser', password='testpassword')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina'))

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password1': 'password123', 'password2': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_carrello_view(self):
        response = self.client.get(reverse('carrello'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carrello')

    def test_update_quantita_view(self):
        response = self.client.post(reverse('update_quantita', args=[self.prodotto.codice_seriale]), {'quantita_acquisto': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carrello'))

        prodotto_carrello = ProdottoCarrello.objects.get(id=self.prodotto_carrello.id)
        self.assertEqual(prodotto_carrello.quantita_acquisto, 3)

    def test_aggiungi_al_carrello_view(self):
        response = self.client.get(reverse('aggiungi_al_carrello', args=[self.prodotto.codice_seriale, 2]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina'))

        prodotto_carrello = ProdottoCarrello.objects.filter(utente=self.utente, prodotto=self.prodotto).first()
        self.assertIsNotNone(prodotto_carrello)
        self.assertEqual(prodotto_carrello.quantita_acquisto, 2)

    def test_rimuovi_dal_carrello_view(self):
        response = self.client.get(reverse('rimuovi_dal_carrello', args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carrello'))

        prodotto_carrello = ProdottoCarrello.objects.filter(utente=self.utente, prodotto=self.prodotto).first()
        self.assertIsNone(prodotto_carrello)

    def test_ordine_view(self):
        response = self.client.get(reverse('ordine'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('ordine'), {'indirizzo': 'Via Prova 123', 'pagamento': 'Carta di credito'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina'))

        nuovo_ordine = Ordine.objects.filter(cliente=self.utente).first()
        self.assertIsNotNone(nuovo_ordine)

if __name__ == '__main__':
    unittest.main()
