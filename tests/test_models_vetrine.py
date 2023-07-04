import unittest
from django.test import TestCase
from .models import Vetrina, VetrinaAmministratore

class VetrinaTest(unittest.TestCase):
    def test_str_method(self):
        vetrina = Vetrina.objects.create(ID_vetrina='Test Vetrina')
        self.assertEqual(str(vetrina), 'Test Vetrina')

    def test_save_creates_vetrina_amministratore(self):
        vetrina = Vetrina.objects.create(ID_vetrina='Test Vetrina')
        vetrina_amministratore = VetrinaAmministratore.objects.get(vetrina=vetrina)
        self.assertEqual(vetrina_amministratore.vetrina, vetrina)

class VetrinaAmministratoreTest(unittest.TestCase):
    def test_str_method(self):
        vetrina_amministratore = VetrinaAmministratore.objects.create(ID_vetrina_admin='Test Vetrina Amministratore')
        self.assertEqual(str(vetrina_amministratore), 'Test Vetrina Amministratore')

if __name__ == '__main__':
    unittest.main()
