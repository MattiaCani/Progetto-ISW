import unittest
import os

# Importa tutti i moduli contenenti i test
from test_forms_ordini_utente import FormsOrdiniTestCase
from test_forms_prodotti_vetrine import FormsProdottiTestCase
from test_models_utente import UtenteTest, ProdottoTest, \
    ProdottoCarrelloTest, CarrelloTest, PagamentoTest, OrdineTest
from test_models_vetrine import VetrinaTest, VetrinaAmministratoreTest
from test_views_utente import UtenteViewsTestCase
from test_views_vetrine import VetrineViewsTestCase

# Aggiungi qui gli altri moduli di test che desideri eseguire

if __name__ == "__main__":
    # Crea una suite di test
    test_suite = unittest.TestSuite()

    # aggiunta dei moduli di test

    # moduli test FORMS
    unittest.TestLoader.loadTestsFromTestCase(FormsOrdiniTestCase)
    unittest.TestLoader.loadTestsFromTestCase(FormsProdottiTestCase)

    # moduli test MODELS
    unittest.TestLoader.loadTestsFromTestCase(UtenteTest)
    unittest.TestLoader.loadTestsFromTestCase(ProdottoTest)
    unittest.TestLoader.loadTestsFromTestCase(ProdottoCarrelloTest)
    unittest.TestLoader.loadTestsFromTestCase(CarrelloTest)
    unittest.TestLoader.loadTestsFromTestCase(PagamentoTest)
    unittest.TestLoader.loadTestsFromTestCase(OrdineTest)
    unittest.TestLoader.loadTestsFromTestCase(VetrinaTest)
    unittest.TestLoader.loadTestsFromTestCase(VetrinaAmministratoreTest)

    # moduli test VIEWS
    unittest.TestLoader.loadTestsFromTestCase(UtenteViewsTestCase)
    unittest.TestLoader.loadTestsFromTestCase(VetrineViewsTestCase)

    #  Runner del test
    runner = unittest.TextTestRunner()

    # Esecuzione dei test
    result = runner.run(test_suite)

    # Verifica se ci sono errori o fallimenti nei test
    if result.errors or result.failures:
        exit(1)
    else:
        exit(0)
