import unittest
import json
from django.test import TestCase
from datetime import datetime
from utente.models import Utente, Prodotto, ProdottoCarrello, Carrello, Pagamento, Ordine
from vetrine.models import Vetrina, VetrinaAmministratore, ResocontoVendite


# test della creazione di un utente e verifica del relativo carrello associato #test ok
class UtenteTest(TestCase):
    def test_save_creates_carrello(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        carrello = Carrello.objects.get(possessore=utente)
        self.assertEqual(carrello.possessore, utente)

# test creazione di un prodotto e verifica della quantità #test ok

class ProdottoTest(TestCase):
    def setUp(self):
        self.prodotto = Prodotto.objects.create(
            nome='Prodotto di test',
            codice_seriale=12345,
            tipologia='Test',
            descrizione='Descrizione di test',
            prezzo=9.99,
            disponibilita=10
        )

    def test_creazione_prodotto(self):
        self.assertEqual(self.prodotto.nome, 'Prodotto di test')
        self.assertEqual(self.prodotto.codice_seriale, 12345)
        self.assertEqual(self.prodotto.tipologia, 'Test')
        self.assertEqual(self.prodotto.descrizione, 'Descrizione di test')
        self.assertEqual(self.prodotto.prezzo, 9.99)
        self.assertEqual(self.prodotto.disponibilita, 10)

    def test_aggiunta_quantita_venduta(self):
        self.assertEqual(self.prodotto.pezzi_venduti, 0)
        self.prodotto.pezzi_venduti = 5
        self.assertEqual(self.prodotto.pezzi_venduti, 5)

    def test_riduzione_disponibilita(self):
        self.assertEqual(self.prodotto.disponibilita, 10)
        self.prodotto.disponibilita -= 3
        self.assertEqual(self.prodotto.disponibilita, 7)

    def test_guadagno_totale(self):
        self.assertEqual(self.prodotto.guadagno_totale, 0)
        self.prodotto.pezzi_venduti = 5
        self.assertEqual(self.prodotto.guadagno_totale, 49.95)  # 5 * 9.99

    def tearDown(self):
        self.prodotto.delete()

# test di aggiunta di un prodotto al carrello #test ok
class ProdottoCarrelloTest(TestCase):
    def test_str_method(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        vetrina = Vetrina.objects.create(ID_vetrina='Test Vetrina')
        resoconto = ResocontoVendite.objects.create(ID_resoconto='Test Resoconto')
        prodotto = Prodotto.objects.create(
            nome='Test Prodotto',
            codice_seriale=1,
            vetrina=vetrina,
            resoconto_vendite=resoconto
        )
        prodotto_carrello = ProdottoCarrello.objects.create(utente=utente, prodotto=prodotto)
        self.assertEqual(str(prodotto_carrello), str(prodotto))


# test creazione di un carrello
class CarrelloTest(TestCase): #test ok
    def test_str_method(self):
        utente = Utente.objects.create(username='testuser', email='test@example.com')
        carrello, _ = Carrello.objects.get_or_create(possessore=utente)
        self.assertEqual(carrello.__str__(), 'testuser')

# test impostazione e verifica del pagamento
class PagamentoTest(TestCase): #test ok
    def test_str_method(self):
        pagamento = Pagamento.objects.create(numero_carta=1234567890)
        self.assertEqual(pagamento.numero_carta, 1234567890)

# test di creazione di un ordine #test ok
class OrdineTest(TestCase):
    def test_str_method(self):
        ordine, _ = Ordine.objects.get_or_create(
            numero_ordine='1',
            carrello=json.dumps([]),
            data_ordine=datetime.now(),
            numero_carta='1234567890'  # Fornisci un numero di carta valido qui
        )
        self.assertEqual(ordine.numero_ordine, '1')

if __name__ == '__main__':
    unittest.main()