from rest_framework.test import APITestCase

# Create your tests here.


class StaticUrlTests(APITestCase):
    def test_renumber_endpoint(self):
        response = self.client.get("/catalog/re/10/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_converter_endpoint(self):
        response = self.client.get("/catalog/converter/10/")
        self.assertEqual(response.status_code, 200)
