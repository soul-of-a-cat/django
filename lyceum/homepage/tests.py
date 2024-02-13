from rest_framework.test import APITestCase


class StaticUrlTests(APITestCase):
    def test_homepage_endpoint(self):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = self.client.get("/homepage/coffee/")
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode(), "Я чайник")
