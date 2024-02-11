from django.test import Client, TestCase

# Create your tests here.


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/homepage/")
        self.assertEqual(response.status_code, 200)
