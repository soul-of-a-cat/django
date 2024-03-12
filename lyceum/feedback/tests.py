from django.test import Client, TestCase
from django.urls import reverse

import feedback.forms

__all__ = [
    "FormTests",
]


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_name_label(self):
        name_label = self.form.fields["text"].label
        self.assertEqual(name_label, "Текст")

    def test_name_help_text(self):
        name_help_text = self.form.fields["text"].help_text
        self.assertEqual(name_help_text, "Напишите текст сообщения")

    def test_create_task(self):
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
