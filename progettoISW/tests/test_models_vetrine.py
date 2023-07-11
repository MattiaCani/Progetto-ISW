import unittest
from django.test import TestCase
from vetrine.models import Vetrina, VetrinaAmministratore, inizializza_vetrine


class VetrinaTestCase(TestCase):
    def test_creazione_vetrina(self):
        vetrina = Vetrina.objects.create(ID_vetrina='Vetrina di test')

        self.assertEqual(vetrina.ID_vetrina, 'Vetrina di test')
        self.assertEqual(VetrinaAmministratore.objects.filter(vetrina=vetrina).count(), 1)

    def test_creazione_vetrina_amministratore(self):
        vetrina_amministratore = VetrinaAmministratore.objects.create(ID_vetrina_admin='Vetrina Amministratore di test')

        self.assertEqual(vetrina_amministratore.ID_vetrina_admin, 'Vetrina Amministratore di test')

    def test_inizializza_vetrine(self):
        inizializza_vetrine()

        self.assertIsNotNone(Vetrina.objects.get(ID_vetrina='Vetrina'))
        self.assertIsNotNone(VetrinaAmministratore.objects.get(ID_vetrina_admin='Vetrina Amministratore'))

    def test_str(self):
        vetrina = Vetrina.objects.create(ID_vetrina='Vetrina di test')
        vetrina_amministratore = VetrinaAmministratore.objects.create(ID_vetrina_admin='Vetrina Amministratore di test')

        self.assertEqual(str(vetrina), 'Vetrina di test')
        self.assertEqual(str(vetrina_amministratore), 'Vetrina Amministratore di test')

if __name__ == '__main__':
    unittest.main()
