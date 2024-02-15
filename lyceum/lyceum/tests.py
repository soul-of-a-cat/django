from django.test import Client, override_settings, TestCase


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = [
            Client().get("/coffee/").content.decode() for _ in range(10)
        ]
        self.assertIn("Я кинйач", contents)
        self.assertEqual(contents.count("Я кинйач"), 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_desabled(self):
        contents = [
            Client().get("/coffee/").content.decode() for _ in range(10)
        ]
        self.assertNotIn("Я кинйач", contents)
