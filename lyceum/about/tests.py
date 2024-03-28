from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        url = reverse("about:description")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
