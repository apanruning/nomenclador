from django.test import TestCase
from django.test.client import Client

class TestsForPageExistence:
    def test_exists(self):
        c = Client()
        response = c.get(self.page)
        self.assertEqual(response.status_code, 200)

class Login(TestCase, TestsForPageExistence):
    page = '/accounts/login/'

class LogOut(TestCase, TestsForPageExistence):
    page = '/accounts/logout/'

class Profile(TestCase, TestsForPageExistence):
    page = '/accounts/profile/'

