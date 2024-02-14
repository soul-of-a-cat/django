from django.test import override_settings
from rest_framework.test import APITestCase


class ReverseResponseMiddlewareTests(APITestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = [
            self.client.get("/coffee/").content.decode() for _ in range(10)
        ]
        self.assertIn("Я кинйач", contents)
        self.assertEqual(contents.count("Я кинйач"), 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = [
            self.client.get("/coffee/").content.decode() for _ in range(10)
        ]
        self.assertNotIn("Я кинйач", contents)
