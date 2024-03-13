from django import forms

from feedback.models import Feedback

__all__ = [
    "FeedbackForm",
]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback

        exclude = [
            Feedback.created_on.field.name,
            Feedback.status.field.name,
        ]

        fields = (
            Feedback.name.field.name,
            Feedback.text.field.name,
            Feedback.mail.field.name,
        )

        labels = {
            Feedback.name.field.name: "Имя",
            Feedback.text.field.name: "Текст",
            Feedback.mail.field.name: "Почта",
        }

        help_texts = {
            Feedback.name.field.name: "Напишите своё имя",
            Feedback.text.field.name: "Напишите текст сообщения",
            Feedback.mail.field.name: "Почтовый адрес",
        }

        widgets = {
            Feedback.text.field.name: forms.TextInput(
                attrs={"class": "my-field"},
            ),
        }

        error_messages = {
            Feedback.name.field.name: {
                "required": "Please enter your name",
            },
            Feedback.text.field.name: {
                "required": "Please enter text",
            },
            Feedback.mail.field.name: {
                "required": "Please enter your email",
            },
        }
