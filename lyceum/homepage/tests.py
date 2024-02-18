from rest_framework import status
from rest_framework.test import APITestCase


class StaticUrlTests(APITestCase):
    def test_homepage_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coffee_endpoint(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")
