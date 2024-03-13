from django.test import Client, TestCase
from django.urls import reverse

import feedback.models
from feedback.models import Feedback

__all__ = [
    "FormTests",
]


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.models.FeedbackForm()

    def test_name_label(self):
        name_label = self.form.fields["text"].label
        self.assertEqual(name_label, "Текст")

    def test_name_help_text(self):
        name_help_text = self.form.fields["text"].help_text
        self.assertEqual(name_help_text, "Напишите текст сообщения")

    def test_redirect(self):
        form_data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "sgadfh@mail.ru",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_errors(self) -> None:
        data = {"text": "some text", "mail": "wrong email"}
        feedback_count = Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertFormError(
            response,
            "form",
            "mail",
            "Введите правильный адрес электронной почты.",
        )
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count,
            "Feedback created while validation failed",
        )

    def test_form_add_db(self):
        feedback_count = Feedback.objects.count()
        form_data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "sgadfh@mail.ru",
        }
        Client().post(
            reverse("feedback:feedback"),
            form_data,
            follow=True,
        )
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count + 1,
            "Feedback created while validation failed",
        )
