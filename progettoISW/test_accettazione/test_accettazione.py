import json

import time
import unittest
from types import SimpleNamespace
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By

from test_accettazione import utility_test
from test_accettazione.AddToCartTest import AddToCartTestFunctions

from test_accettazione.AdminLoginTest import AdminLoginTestFunctions
from test_accettazione.CheckoutTest import CheckoutTestFunctions
from test_accettazione.ClientLoginTest import ClientLoginTestFunctions
from test_accettazione.ClientSignUpTest import ClientSignUpTestFunctions
from test_accettazione.FilterTest import FilterTestFunctions
from test_accettazione.LogoutTest import LogoutTestFunctions
from test_accettazione.ProductsTest import ProductsTestFunctions
from test_accettazione.ReportTest import ReportTestFunctions
from test_accettazione.SearchTest import SearchTestFunction
from utente.models import Utente, Prodotto
from vetrine.models import inizializza_vetrine


class SeleniumTest(StaticLiveServerTestCase):
    user_test = "user_test"
    admin_test = "admin_test"

    def test_logout(self):
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        Utente.objects.create_user(username=self.user_test, password=self.user_test, email="testu@testu.testu")
        Utente.objects.create_superuser(username=self.admin_test, password=self.admin_test, email="testa@testa.testa")

        credentials = [self.user_test, self.admin_test]

        for user in credentials:
            utility_test.login(self.selenium, user, user)

            time.sleep(1)

            LogoutTestFunctions.logout(self.selenium)

            time.sleep(1)

        self.selenium.quit()

    def test_client_signup(self):
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}/signup/")

        test_data = []

        with open('test_accettazione/ClientSignUpTest/ClientSignUpTestData') as user_list:
            for json_user in user_list:
                test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

        time.sleep(1)

        for user in test_data:
            if user.test == "reg_success":
                ClientSignUpTestFunctions.reg_success(self.selenium, user)
                self.selenium.delete_all_cookies()
                self.selenium.get(f"{self.live_server_url}/signup/")
                time.sleep(1)
            elif user.test == "reg_email_failure":
                ClientSignUpTestFunctions.reg_email_failure(self.selenium, user)
                time.sleep(1)
            elif user.test == "reg_username_failure":
                ClientSignUpTestFunctions.reg_username_failure(self.selenium, user)
                time.sleep(1)
            elif user.test == "reg_different_passwords":
                ClientSignUpTestFunctions.reg_different_passwords(self.selenium, user)
                time.sleep(1)
            elif user.test == "reg_problem_password":
                ClientSignUpTestFunctions.reg_problem_password(self.selenium, user)
                time.sleep(1)

        self.selenium.quit()

    def test_client_login(self):
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        test_data = []

        with open('test_accettazione/ClientLoginTest/ClientLoginTestData') as user_list:
            for json_user in user_list:
                test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

        Utente.objects.create_user(username="Test2", password="soffitto9H1", email="ksjfdha@ajlksdf.com")
        Utente.objects.create_user(username="Test3", password="pavimento9H1", email="oiseljef@alksdf.com")

        time.sleep(1)

        for user in test_data:
            if user.test == "log_success":
                ClientLoginTestFunctions.log_success(self.selenium, user)
                self.selenium.delete_all_cookies()
                self.selenium.back()
                time.sleep(1)
            elif user.test == "log_username_failure":
                ClientLoginTestFunctions.log_username_failure(self.selenium, user)
                time.sleep(1)
            elif user.test == "log_pass_failure":
                ClientLoginTestFunctions.log_pass_failure(self.selenium, user)
                time.sleep(1)

        self.selenium.quit()

    def test_add_to_cart(self):
        inizializza_vetrine()
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        Utente.objects.create_user(username=self.user_test, password=self.user_test, email="testu@testu.testu")
        Prodotto.objects.create(disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=10.0)

        utility_test.login(self.selenium, self.user_test, self.user_test)

        time.sleep(1)

        AddToCartTestFunctions.add_new_product(self, self.selenium, "Prodotto 1", "5")
        time.sleep(1)
        AddToCartTestFunctions.change_quantity(self, self.selenium, "Prodotto 1", "9")
        time.sleep(1)
        AddToCartTestFunctions.add_product(self.selenium, "Prodotto 1")
        time.sleep(1)
        AddToCartTestFunctions.remove_product(self, self.selenium, "Prodotto 1")

        self.selenium.quit()

    def test_admin_login(self):
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        test_data = []

        with open('test_accettazione/AdminLoginTest/AdminLoginTestData') as admin_list:
            for json_admin in admin_list:
                test_data.append(json.loads(json_admin, object_hook=lambda d: SimpleNamespace(**d)))

        Utente.objects.create_superuser(username="admin", password="admin", email="ksjfdha@ajlksdf.com")
        Utente.objects.create_superuser(username="unica", password="unica", email="oiseljef@alksdf.com")

        time.sleep(1)

        for admin in test_data:
            if admin.test == "log_success":
                AdminLoginTestFunctions.a_log_success(self.selenium, admin)
                self.selenium.delete_all_cookies()
                self.selenium.back()
                time.sleep(1)
            elif admin.test == "log_username_failure":
                AdminLoginTestFunctions.a_log_email_failure(self.selenium, admin)
                time.sleep(1)
            elif admin.test == "log_pass_failure":
                AdminLoginTestFunctions.a_log_pass_failure(self.selenium, admin)
                time.sleep(1)

        self.selenium.quit()

    def test_checkout(self):
        inizializza_vetrine()
        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        Utente.objects.create_user(username=self.user_test, password=self.user_test, email="testu@testu.testu")
        utility_test.login(self.selenium, self.user_test, self.user_test)

        Prodotto.objects.create(disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=10.0)

        self.selenium.get(f"{self.live_server_url}/vetrina/")
        product = self.selenium.find_element(By.ID, "Prodotto 1")
        add_product = product.find_element(By.NAME, "add_product")
        add_product.click()

        time.sleep(1)

        cart_products = CheckoutTestFunctions.get_cart_products(self, self.selenium)
        CheckoutTestFunctions.cancel_order(self, self.selenium, cart_products)

        time.sleep(1)

        cart_products = CheckoutTestFunctions.get_cart_products(self, self.selenium)
        CheckoutTestFunctions.confirm_order(self, self.selenium, cart_products)

        self.selenium.quit()

    def test_search(self):
        inizializza_vetrine()

        Prodotto.objects.create(pezzi_venduti="0", disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=10.0)

        Utente.objects.create_user(username=self.user_test, password=self.user_test, email="testu@testu.testu")

        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        utility_test.login(self.selenium, self.user_test, self.user_test)

        time.sleep(1)

        SearchTestFunction.search_success(self.selenium, "Prodotto")
        SearchTestFunction.search_failure(self.selenium, "adfadsf")

        time.sleep(1)

        self.selenium.quit()

    def test_filter(self):
        inizializza_vetrine()

        Prodotto.objects.create(pezzi_venduti="0", disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=10.0)
        Prodotto.objects.create(pezzi_venduti="85", disponibilita="500", nome='Prodotto 2', codice_seriale=2,
                                tipologia="Tipologia prodotto 2", descrizione="Descrizione prodotto",
                                prezzo=150.0)
        Prodotto.objects.create(pezzi_venduti="66", disponibilita="5", nome='Prodotto 3', codice_seriale=3,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=70.0)

        Utente.objects.create_user(username=self.user_test, password=self.user_test, email="testu@testu.testu")

        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        utility_test.login(self.selenium, self.user_test, self.user_test)

        time.sleep(1)

        original_products = FilterTestFunctions.get_products(self.selenium)

        FilterTestFunctions.add_filter(self.selenium, "tipologia", "Tipologia prodotto")
        FilterTestFunctions.remove_filter(self.selenium, "tipologia")

        FilterTestFunctions.add_filter(self.selenium, "disponibilita", "Disponibile")
        FilterTestFunctions.remove_filter(self.selenium, "disponibilita")

        FilterTestFunctions.add_filter(self.selenium, "prezzo_min", 20)
        FilterTestFunctions.remove_filter(self.selenium, "prezzo_min")

        FilterTestFunctions.add_filter(self.selenium, "prezzo_max", 60)
        FilterTestFunctions.remove_filter(self.selenium, "prezzo_max")

        FilterTestFunctions.remove_all_filter(self.selenium, original_products)

        time.sleep(1)

        self.selenium.quit()

    def test_product(self):
        inizializza_vetrine()

        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        Utente.objects.create_superuser(username=self.admin_test, password=self.admin_test, email="testu@testu.testu")
        utility_test.login(self.selenium, self.admin_test, self.admin_test)

        test_data = []

        with open('test_accettazione/CheckoutTest/CheckoutTestData') as user_list:
            for json_user in user_list:
                test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

        time.sleep(1)

        ProductsTestFunctions.insert_product_success(self.selenium, test_data[0])
        ProductsTestFunctions.insert_product_failure(self, self.selenium, test_data[1])

        ProductsTestFunctions.modify_product_failure(self, self.selenium, test_data[0], -50)
        ProductsTestFunctions.modify_product_success(self.selenium, test_data[0], 6565984)

        ProductsTestFunctions.remove_product_success(self.selenium, test_data[0])

        self.selenium.quit()

    def test_report(self):
        inizializza_vetrine()

        Prodotto.objects.create(pezzi_venduti="0", disponibilita="100", nome='Prodotto 1', codice_seriale=1,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=10.0)
        Prodotto.objects.create(pezzi_venduti="85", disponibilita="500", nome='Prodotto 2', codice_seriale=2,
                                tipologia="Tipologia prodotto 2", descrizione="Descrizione prodotto",
                                prezzo=150.0)
        Prodotto.objects.create(pezzi_venduti="66", disponibilita="5", nome='Prodotto 3', codice_seriale=3,
                                tipologia="Tipologia prodotto", descrizione="Descrizione prodotto",
                                prezzo=70.0)

        Utente.objects.create_superuser(username=self.admin_test, password=self.admin_test, email="testu@testu.testu")

        self.selenium = WebDriver()
        self.selenium.get(f"{self.live_server_url}")

        utility_test.login(self.selenium, self.admin_test, self.admin_test)

        time.sleep(1)

        ReportTestFunctions.open_report(self, self.selenium)

        time.sleep(1)

        original_products = FilterTestFunctions.get_products(self.selenium)

        FilterTestFunctions.add_filter(self.selenium, "tipologia", "Tipologia prodotto")
        FilterTestFunctions.remove_filter(self.selenium, "tipologia")

        FilterTestFunctions.add_filter(self.selenium, "disponibilita", "Disponibile")
        FilterTestFunctions.remove_filter(self.selenium, "disponibilita")

        FilterTestFunctions.add_filter(self.selenium, "prezzo_min", 20)
        FilterTestFunctions.remove_filter(self.selenium, "prezzo_min")

        FilterTestFunctions.add_filter(self.selenium, "prezzo_max", 80)
        FilterTestFunctions.remove_filter(self.selenium, "prezzo_max")

        FilterTestFunctions.remove_all_filter(self.selenium, original_products)

        self.selenium.quit()


if __name__ == '__main__':
    unittest.main()
