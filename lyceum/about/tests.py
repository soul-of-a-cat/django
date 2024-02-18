from rest_framework import status
from rest_framework.test import APITestCase


class StaticUrlTests(APITestCase):
    def test_about_endpoint(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
