from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        url = reverse("homepage:home")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        url = reverse("homepage:coffee")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")
