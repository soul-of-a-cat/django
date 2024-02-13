from rest_framework.test import APITestCase

# Create your tests here.


class StaticUrlTests(APITestCase):
    def test_renumber_endpoint(self):
        response = self.client.get("/catalog/re/1")
        self.assertEqual(response.content.decode(), response.content.decode())

    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)
