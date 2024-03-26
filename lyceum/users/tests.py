import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import users.models


__all__ = [
    "UserTests",
]


class UserTests(TestCase):
    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_positive(self):
        self.assertFalse(User.objects.exists())
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertFalse(User.objects.first().is_active)
        self.client.get(reverse("users:activate", args=[1]))
        self.assertTrue(User.objects.first().is_active)

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_negative(self):
        self.assertFalse(User.objects.exists())
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertFalse(User.objects.first().is_active)
        expired_dt = timezone.now() + datetime.timedelta(hours=13)
        with patch("django.utils.timezone.now") as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(reverse("users:activate", args=[1]))
            self.assertFalse(User.objects.first().is_active)

    def test_user_signup_positive(self):
        self.assertFalse(User.objects.exists())
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertTrue(User.objects.exists())
        self.assertEqual(User.objects.first().username, "test_username")

    def test_user_signup_negative(self):
        self.assertFalse(User.objects.exists())
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "simple",
                "password2": "simple",
            },
        )
        self.assertFalse(User.objects.exists())

    def test_user_signup_identical_emails(self):
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username1",
                "email": "qwerty@mail.ru",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username2",
                "email": "qwerty@mail.ru",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertEqual(User.objects.count(), 1)

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_login_email_or_username(self):
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "email": "qwerty@mail.ru",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.client.get(reverse("users:activate", args=[1]))
        self.client.post(
            reverse("users:login"),
            data={
                "username": "test_username",
                "password": "VeryStr0ngPa$$",
            },
        )
        self.assertEqual(
            timezone.now().strftime("%d/%m/%Y %H:%M"),
            User.objects.first().last_login.strftime("%d/%m/%Y %H:%M"),
        )
        self.client.get(reverse("users:logout"))
        self.client.post(
            reverse("users:login"),
            data={
                "username": "qwerty@mail.ru",
                "password": "VeryStr0ngPa$$",
            },
        )
        self.assertEqual(
            timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
            User.objects.first().last_login.strftime("%d/%m/%Y %H:%M:%S"),
        )

    def test_block_user(self):
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.client.get(reverse("users:activate", args=[1]))
        for _ in range(11):
            self.client.post(
                reverse("users:login"),
                data={
                    "username": "test_username",
                    "password": "wrong",
                },
            )

        self.assertEqual(
            users.models.Profile.objects.first().attempts_count,
            11,
        )
        now_time = timezone.now().strftime("%d/%m/%Y %H:%M")
        profile = users.models.Profile.objects.first()
        self.assertEqual(
            now_time,
            profile.block_date.strftime("%d/%m/%Y %H:%M"),
        )
        self.assertFalse(User.objects.first().is_active)
        expired_dt = timezone.now() + datetime.timedelta(days=8)
        with patch("django.utils.timezone.now") as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(reverse("users:activate", args=[1]))
            self.assertFalse(User.objects.first().is_active)

    def test_user_reactive(self):
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.client.get(reverse("users:activate", args=[1]))
        for _ in range(11):
            self.client.post(
                reverse("users:login"),
                data={
                    "username": "test_username",
                    "password": "wrong",
                },
            )

        self.client.get(reverse("users:reactivate", args=[1]))
        self.assertTrue(User.objects.first().is_active)
