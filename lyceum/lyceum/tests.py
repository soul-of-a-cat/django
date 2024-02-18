from django.test import override_settings
from rest_framework.test import APITestCase


class ReverseResponseMiddlewareTests(APITestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {}
        for i in range(10):
            content = self.client.get("/coffee/").content.decode()
            contents[content] = contents.get(content, 0) + 1
        self.assertEqual(contents["Я чайник"], 9)
        self.assertEqual(contents["Я кинйач"], 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {}
        for _ in range(10):
            content = self.client.get("/coffee/").content.decode()
            contents[content] = contents.get(content, 0) + 1
        self.assertNotIn("Я кинйач", contents)
