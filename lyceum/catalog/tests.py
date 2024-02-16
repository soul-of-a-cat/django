from rest_framework import status
from rest_framework.test import APITestCase


class StaticUrlTests(APITestCase):
    def test_renumber_endpoint(self):
        response = self.client.get("/catalog/re/10/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_converter_endpoint(self):
        response = self.client.get("/catalog/converter/10/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renumber_negative_endpoint(self):
        response = self.client.get("/catalog/re/-10/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_renumber_zero_endpoint(self):
        response = self.client.get("/catalog/re/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_renumber_wrong_endpoint(self):
        response = self.client.get("/catalog/re/0123/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_converter_negative_endpoint(self):
        response = self.client.get("/catalog/converter/-10/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_converter_zero_endpoint(self):
        response = self.client.get("/catalog/converter/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_converter_wrong_endpoint(self):
        response = self.client.get("/catalog/converter/0123/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
