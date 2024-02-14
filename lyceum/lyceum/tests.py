from django.test import override_settings
from rest_framework.test import APITestCase


class MiddleWareTests(APITestCase):
    @override_settings(
        MIDDLEWARE=("lyceum.middleware.ReverseResponseMiddleware",)
    )
    def test_reverse_russian_words_enabled(self):
        for i in range(10):
            response = self.client.get("/homepage/coffee/")
            if i == 9:
                self.assertIn("Я кинйач".encode(), response.content)

    @override_settings(ALLOW_REVERSE=False)
    def test_disabled_reverse_middleware(self):
        for i in range(10):
            response = self.client.get("/homepage/coffee/")
            if i == 9:
                self.assertIn("Я чайник".encode(), response.content)

    @override_settings(
        MIDDLEWARE=("lyceum.middleware.ReverseResponseMiddleware",)
    )
    def test_reverse_russian_words_enabled_default(self):
        for i in range(10):
            response = self.client.get("/homepage/coffee/")
            if i == 9:
                self.assertIn("Я кинйач".encode(), response.content)
