import unittest
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import vetrine.views
from django.test import Client, TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from vetrine.models import Vetrina, VetrinaAmministratore
from utente.models import Utente, Prodotto, inizializza_vetrine, ResocontoVendite, Ordine
from vetrine.views import vetrina_cliente_view, vetrina_amministratore_view, rimuovi_prodotto_view, modifica_prodotto_view, resoconto_vendite_view
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Prodotto.objects.all().delete()
        self.client = Client()
        self.user = Utente.objects.create(username='testuser', email='t@example.com')
        model = get_user_model()
        self.superuser = model.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword')
        self.vetrina, _ = Vetrina.objects.get_or_create(ID_vetrina='Test Vetrina')
        self.prodotto = Prodotto.objects.create(
            nome='Test Prodotto',
            codice_seriale=1,
            tipologia='Test Tipologia',
            descrizione='Test Descrizione',
            prezzo=10.0,
            vetrina=self.vetrina
        )
        self.codice_seriale = self.prodotto.codice_seriale

        self.ordine, _ = Ordine.objects.get_or_create(
            cliente = self.user,
            numero_ordine=1,
            data_ordine='2021-01-01',
            numero_carta=1234567890,
            carrello=json.dumps([]),
            indirizzo_spedizione='Via Prova 1',
            intestatario='Test User',
            nome_metodo='CREDITO'
        )

        self.numero_ordine = self.ordine.numero_ordine


    def test_vetrina_cliente_view(self):
        # Effettua il login con le credenziali di test
        self.client.force_login(self.user)

        # Effettua la richiesta GET alla vista 'vetrina'
        response = self.client.get(reverse('vetrina'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vetrine/vetrina.html')
        self.assertContains(response, 'Test Prodotto', html=False)

    def test_vetrina_amministratore_view(self):

        # Effettua il login come utente superuser
        self.client.force_login(self.superuser)

        response = self.client.get(reverse('vetrina_amministratore'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Prodotto', html=False)
        self.assertTemplateUsed(response, 'vetrine/vetrinaAmministratore.html')

    def test_nuovo_prodotto_view(self):
        self.client.force_login(self.superuser)
        prodotto = Prodotto.objects.create(
            nome='Test Prodotto2',
            codice_seriale=2,
            tipologia='Test Tipologia',
            descrizione='Test Descrizione',
            prezzo=10.0,
            vetrina=self.vetrina
        )
        response = self.client.post(reverse('nuovo_prodotto'),
                                    self.client.get(prodotto) ,
                                    follow=True)
        self.assertEqual(response.status_code, 200)  # Verifica il codice di stato 200
        self.assertEqual(Prodotto.objects.count(), 2)
        self.assertContains(response, 'form-control')  # Verifica la presenza del campo del form


    def test_rimuovi_prodotto_view(self):
        self.client.force_login(self.superuser)

        request = self.factory.get(reverse('rimuovi_prodotto', args=[self.codice_seriale]))
        request.user = self.superuser

        #print(f"Codice seriale del prodotto: {self.codice_seriale}")
        response = rimuovi_prodotto_view(request, self.codice_seriale)
        #print(f"Response status code: {response.status_code}")

        prodotto_esistente = Prodotto.objects.filter(codice_seriale=self.codice_seriale).exists()
        #print(f"Esiste ancora un prodotto con il codice seriale {self.codice_seriale}: {prodotto_esistente}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prodotto.objects.count(), 0)

    def test_modifica_prodotto_view(self):
        # Simula una richiesta POST con dati di modifica validi
        url = reverse('modifica_prodotto', args=[self.codice_seriale])
        data = {
            'nome': 'Prodotto modificato',
            'tipologia': 'Tipologia modificata',
            'descrizione': 'Descrizione modificata',
            'prezzo': 19.99,
            'disponibilita': 5
        }
        request = self.factory.post(url, data)
        request.user = self.superuser

        response = modifica_prodotto_view(request, self.codice_seriale)

        # Verifica che il reindirizzamento sia avvenuto correttamente
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('vetrina_amministratore'))

        # Verifica che il prodotto sia stato modificato nel database
        prodotto_modificato = Prodotto.objects.get(codice_seriale=self.codice_seriale)
        self.assertEqual(prodotto_modificato.nome, 'Prodotto modificato')
        self.assertEqual(prodotto_modificato.tipologia, 'Tipologia modificata')
        self.assertEqual(prodotto_modificato.descrizione, 'Descrizione modificata')
        self.assertEqual(prodotto_modificato.prezzo, 19.99)
        self.assertEqual(prodotto_modificato.disponibilita, 5)

    def test_resoconto_vendite_view(self):
        self.client.force_login(self.superuser)

        resoconto_vendite = ResocontoVendite.objects.get()

        response = self.client.get(reverse('resoconto_vendite'))

        self.assertEqual(response.status_code, 200)

        # Verifica il contesto della risposta
        self.assertIn('ordini', response.context)
        self.assertIn('prodotti', response.context)
        self.assertIn('resoconto_vendite', response.context)
        # Verifica altre variabili nel contesto se necessario

        # Verifica il rendering del template corretto
        self.assertTemplateUsed(response, 'vetrine/resocontoVendite.html')

    def test_dettaglio_ordine_view(self):
        self.client.force_login(self.superuser)
        # Effettua la richiesta GET alla vista dettaglio_ordine_view
        url = reverse('dettaglio_ordine', args=[self.numero_ordine])
        response = self.client.get(url)

        # Verifica che la risposta sia corretta e lo status code sia 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica che l'ordine passato al template sia corretto
        self.assertEqual(response.context['ordine'], self.ordine)

        # Verifica che il template corretto sia utilizzato nella risposta
        self.assertTemplateUsed(response, 'vetrine/dettaglioOrdine.html')


if __name__ == '__main__':
    unittest.main()