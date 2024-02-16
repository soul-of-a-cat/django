from django.test import Client, TestCase
from rest_framework import status


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get("/about/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
