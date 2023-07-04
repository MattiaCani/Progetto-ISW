import unittest
from django.test import TestCase
from .models import Utente, Prodotto, ProdottoCarrello, Carrello, Pagamento, Ordine

# test della creazione di un utente e verifica del relativo carrello associato
class UtenteTest(TestCase):
    def test_save_creates_carrello(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        carrello = Carrello.objects.get(possessore=utente)
        self.assertEqual(carrello.possessore, utente)

# test creazione di un prodotto e verifica della quantità
class ProdottoTest(TestCase):
    def test_str_method(self):
        prodotto = Prodotto.objects.create(nome='Test Prodotto', codice_seriale=1)
        self.assertEqual(str(prodotto), '1')

# test di aggiunta di un prodotto al carrello
class ProdottoCarrelloTest(TestCase):
    def test_str_method(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        prodotto = Prodotto.objects.create(nome='Test Prodotto', codice_seriale=1)
        prodotto_carrello = ProdottoCarrello.objects.create(utente=utente, prodotto=prodotto)
        self.assertEqual(str(prodotto_carrello), str(prodotto))

# test creazione di un carrello
class CarrelloTest(TestCase):
    def test_str_method(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        carrello = Carrello.objects.create(possessore=utente)
        self.assertEqual(str(carrello), 'testuser')

# test impostazione e verifica del pagamento
class PagamentoTest(TestCase):
    def test_str_method(self):
        pagamento = Pagamento.objects.create(numero_carta=1234567890)
        self.assertEqual(str(pagamento), '1234567890')

# test di creazione di un ordine
class OrdineTest(TestCase):
    def test_str_method(self):
        ordine = Ordine.objects.create(numero_ordine=1)
        self.assertEqual(str(ordine), '1')

if __name__ == '__main__':
    unittest.main()