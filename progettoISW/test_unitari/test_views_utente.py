import unittest
import json
from datetime import datetime

from unittest.mock import patch, MagicMock

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from utente import forms
from utente.forms.auth import LoginForm, SignupForm
from utente.models import Utente, Carrello, Prodotto, Ordine, ProdottoCarrello, SessionManager
from vetrine.models import inizializza_vetrine
from utente.forms.forms_ordini import AggiuntaIndirizzo, AggiuntaPagamento, QuantitaProdotto, QuantitaProdottoVetrina
import pdb


class UtenteViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.vetrina_url = reverse('vetrina')
        self.vetrina_admin_url = reverse('vetrina_amministratore')
        self.logout_url = reverse('logout')

        self.signup_url = reverse('signup')
        # Creazione di un utente di prova
        self.username = 'testuser'
        self.password = 'Testpassword#1'
        self.username_admin = "testadmin"
        self.password_admin = 'Adminpassword#1'
        self.user = Utente.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.superuser = Utente.objects.create_superuser(
            username=self.username_admin,
            password=self.password_admin,
            email='admin@admin.com'
        )
        self.ordine_url = reverse('ordine')

        self.valid_data = {
            'username': 'signuser',
            'password1': 'Signpassword#1',
            'password2': 'Signpassword#1',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        inizializza_vetrine()
        self.prodotto = Prodotto.objects.create(disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                                prezzo=10.0)
        self.prodotto_carrello = ProdottoCarrello.objects.create(utente=self.user, prodotto=self.prodotto,
                                                                 quantita_acquisto=2)

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form_login'], forms.auth.LoginForm)

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, self.vetrina_url)
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_success_admin(self):
        response = self.client.post(self.login_url, {
            'username': self.username_admin,
            'password': self.password_admin
        })
        self.assertRedirects(response, self.vetrina_admin_url)
        self.assertEqual(response.status_code, 302)


    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form_login'], forms.auth.LoginForm)
        self.assertEqual(response.context['login_error'], 'Login fallito')


    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_logout_view_admin(self):
        self.client.login(username=self.username_admin, password=self.password_admin)

        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form_registrazione'], forms.auth.SignupForm)

    def test_signup_view_post_valid_form(self):
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Utente.objects.filter(username=self.valid_data['username']).exists())

    def test_signup_view_post_invalid_form(self):
        invalid_data = {
            'username': 'wronguser',
            'password1': 'Testpassword#1',
            'password2': 'DifferentPassword#1',  # Password diversa da quella sopra
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Joe',
        }
        response = self.client.post(self.signup_url, invalid_data)

        # Verifica che la risposta non sia un reindirizzamento, ma un render della stessa pagina di registrazione
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertFalse(response.context['form_registrazione'].is_valid())
        self.assertFalse(Utente.objects.filter(username=invalid_data['username']).exists())

    def test_carrello_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('carrello'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carrello')

    def test_aggiungi_al_carrello_view(self):
        codiceseriale_nuovoprodotto = 100
        self.client.force_login(self.user)
        response = self.client.post(reverse('aggiungi_al_carrello', args=[codiceseriale_nuovoprodotto]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vetrina'))

    def test_update_quantita_view(self):
        self.client.force_login(self.user)
        carrello_utente = Carrello.objects.get(possessore=self.user)
        prodotto_carrello = ProdottoCarrello.objects.get(utente=self.user)
        carrello_utente.lista_prodotti.add(prodotto_carrello)
        carrello_utente.save()
        response = self.client.post(reverse('update_quantita', args=[self.prodotto.codice_seriale]), {'quantita_acquisto': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carrello'))
        prodotto_carrello = ProdottoCarrello.objects.filter(prodotto=self.prodotto).first()
        self.assertIsNotNone(prodotto_carrello)
        self.assertEqual(prodotto_carrello.quantita_acquisto, 3)  # Verifica che la quantità  sia corretta

    def test_rimuovi_dal_carrello_view(self):
        self.client.force_login(self.user)
        carrello_utente = Carrello.objects.get(possessore=self.user)
        prodotto_carrello = ProdottoCarrello.objects.get(utente=self.user)
        carrello_utente.lista_prodotti.add(prodotto_carrello)
        carrello_utente.save()
        response = self.client.get(reverse('rimuovi_dal_carrello', args=[self.prodotto.codice_seriale]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carrello'))


    def test_ordine_view_post_valid_form(self):
        indirizzo_data = {
            'indirizzo_spedizione': 'Via Roma 1',
        }

        pagamento_data = {
            'numero_carta': '1234567890123456',
            'intestatario': 'Mario Rossi',
            'nome_metodo': 'CREDITO',
        }

        form_indirizzo = AggiuntaIndirizzo(initial=indirizzo_data)
        form_pagamento = AggiuntaPagamento(initial=pagamento_data)

        response = self.client.post(self.ordine_url, {**indirizzo_data, **pagamento_data})
        self.assertTrue(Carrello.objects.filter().exists())

    def test_ordine_view_get(self):
        response = self.client.get(self.ordine_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carrello/ordine.html')

        # Verifica che i form siano presenti nel contesto
        self.assertIsInstance(response.context['form_indirizzo'], AggiuntaIndirizzo)
        self.assertIsInstance(response.context['form_pagamento'], AggiuntaPagamento)

if __name__ == '__main__':
    unittest.main()
