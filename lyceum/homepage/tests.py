from django.test import Client, TestCase


# Create your tests here.


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/homepage/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = Client().get("/homepage/coffee/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Я чайник")
