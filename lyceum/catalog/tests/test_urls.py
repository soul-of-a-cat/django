from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        url = reverse("catalog:item-list")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_new_endpoint(self):
        url = reverse("catalog:new")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_friday_endpoint(self):
        url = reverse("catalog:friday")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_unverified_endpoint(self):
        url = reverse("catalog:unverified")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
