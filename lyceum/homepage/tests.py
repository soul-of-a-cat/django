from rest_framework.test import APITestCase
from rest_framework import status


class StaticUrlTests(APITestCase):
    def test_homepage_endpoint(self):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = self.client.get("/homepage/coffee/")
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        self.assertEqual(response.content.decode("utf-8"), "Я чайник")
