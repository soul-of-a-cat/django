from django.test import Client, TestCase, override_settings
from lyceum.middleware import reverse_words
import parameterized


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {}
        for i in range(10):
            content = Client().get("/coffee/").content.decode()
            contents[content] = contents.get(content, 0) + 1
        self.assertEqual(contents["Я чайник"], 9)
        self.assertEqual(contents["Я кинйач"], 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {}
        for _ in range(10):
            content = Client().get("/coffee/").content.decode()
            contents[content] = contents.get(content, 0) + 1
        self.assertNotIn("Я кинйач", contents)

    def test_reverse_russian_words(self):
        contents = {}
        for i in range(10):
            content = Client().get("/coffee/").content.decode()
            contents[content] = contents.get(content, 0) + 1
        self.assertEqual(contents["Я чайник"], 9)
        self.assertEqual(contents["Я кинйач"], 1)


    @parameterized.parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("Я чайникqwerty", "Я чайникqwerty"),
            ("qwerty qwerty", "qwerty qwerty"),
            ("Я чайник1", "Я чайник1"),
            ("Я чайн!ик", "Я чайн!ик"),
        ],
    )
    def test_reverse_worlds(self, word, rev_word):
        rev_words = reverse_words(word)
        self.assertEqual(rev_words.decode(), rev_word)
        self.assertEqual(rev_words.decode(), rev_word)
