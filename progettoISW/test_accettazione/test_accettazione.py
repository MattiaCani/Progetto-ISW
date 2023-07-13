import subprocess
import unittest


class SeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_process = subprocess.Popen(['python', 'manage.py', 'runserver'])

    def test_example(self):
        from test_accettazione.AddToCartTest import AddToCartTest
        from test_accettazione.LogoutTest import LogoutTest
        from test_accettazione.AdminLoginTest import AdminLoginTest
        from test_accettazione.ClientSignUpTest import ClientSignUpTest
        from test_accettazione.FilterTest import FilterTest
        from test_accettazione.SearchTest import SearchTest
        from test_accettazione.CheckoutTest import CheckoutTest
        from test_accettazione.ProductsTest import ProductsTest
        from test_accettazione.ReportTest import ReportTest


if __name__ == '__main__':
    unittest.main()
