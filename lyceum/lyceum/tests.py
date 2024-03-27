import datetime

from django.conf import settings
from django.test import Client, override_settings, TestCase
from django.urls import reverse
import parameterized

import users.models
from lyceum.middleware import reverse_words

__all__ = [
    "ReverseResponseMiddlewareTests",
]


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {}
        for _ in range(10):
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

    def test_reverse_russian_words_enabled_default(self) -> None:
        url = reverse("homepage:coffee")
        contents = [Client().get(url).content.decode() for _ in range(20)]
        msg1 = "No reversed responses by default"
        if settings.ALLOW_REVERSE:
            self.assertIn("Я кинйач", contents, msg1)
        else:
            self.assertNotIn("Я кинйач", contents, msg1)

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled_echo(self):
        form_data = {
            "text": "Привет, этo почтi-почти Pуcский текст@,"
            " просто≈ Как-то со спецü символами:) ¡сорри∑!"
            " Hу ещё раз ¡сорри! Ёжика не видели?",
        }
        contents = {}
        for _ in range(10):
            content = (
                Client()
                .post(
                    reverse("homepage:echo-submit"),
                    form_data,
                    follow=True,
                )
                .content.decode()
            )
            contents[content] = contents.get(content, 0) + 1

        self.assertEqual(
            contents[
                "Привет, этo почтi-почти Pуcский"
                " текст@, просто≈ Как-то со спецü символами:)"
                " ¡сорри∑! Hу ещё раз ¡сорри! Ёжика не видели?"
            ],
            9,
        )
        self.assertEqual(
            contents[
                "тевирП, этo почтi-итчоп Pуcский тскет@, отсорп≈"
                " каК-от ос спецü ималовмис:) ¡иррос∑! Hу ёще зар"
                " ¡иррос! акижЁ ен иледив?"
            ],
            1,
        )

    @parameterized.parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("Я чайникqwerty", "Я чайникqwerty"),
            ("qwerty qwerty", "qwerty qwerty"),
            ("Я чайник1", "Я чайник1"),
            ("Я чайн!ик", "Я нйач!ки"),
        ],
    )
    def test_reverse_worlds(self, word, rev_word):
        rev_words = reverse_words(word)
        self.assertEqual(rev_words, rev_word)
        self.assertEqual(rev_words, rev_word)


class ContextProcessorsTests(TestCase):
    user_register_data = {
        "username": "somethingstrange",
        "email": "abracadabra@ma.ru",
        "password1": "123123123g",
        "password2": "123123123g",
    }

    def test_context_processors_success(self):
        client = Client()

        test_user = users.models.User.objects.create_user(
            username=self.user_register_data["username"]
        )
        users.models.Profile.objects.create(
            user=test_user, birthday=datetime.datetime.now().date()
        )

        response = client.get(reverse("homepage:home"))
        bithday_users = response.context["birthday_users"]
        self.assertTrue(bithday_users)

    def test_context_processors_failed(self):
        client = Client()

        test_user = users.models.User.objects.create_user(
            username=self.user_register_data["username"]
        )
        users.models.Profile.objects.create(
            user=test_user,
            birthday=datetime.datetime.now().date()
            + datetime.timedelta(days=12),
        )

        response = client.get(reverse("homepage:home"))
        bithday_users = response.context["birthday_users"]
        self.assertFalse(bithday_users)
