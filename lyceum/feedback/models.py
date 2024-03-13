from django.db import models
from django import forms

__all__ = [
    "Feedback",
]


class Feedback(models.Model):
    name = models.CharField(
        "имя",
        help_text="Напишите своё имя",
        max_length=100,
        null=True,
    )
    text = models.CharField(
        "текст",
        help_text="Напишите текст сообщения",
        max_length=1000,
    )
    created_on = models.DateTimeField(
        verbose_name="создано",
        help_text="Дата и время создания",
        auto_now_add=True,
        null=True,
    )
    mail = models.EmailField(
        verbose_name="e-mail",
        help_text="Почтовый адрес",
    )
    status = models.CharField(
        verbose_name="status",
        help_text="Статус",
        max_length=100,
        null=True,
    )

    class Meta:
        app_label = "feedback"

    def __str__(self):
        return self.text[:10]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback

        exclude = [Feedback.created_on.field.name]

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
            Feedback.text.field.name: forms.Textarea(
                attrs={"class": "my-field"}
            ),
        }

        error_messages = {
            Feedback.name.field.name: {
                "required": "Please enter your name",
            },
            Feedback.text.field.name: {
                "required": "Please enter your name",
            },
            Feedback.mail.field.name: {
                "required": "Please enter your name",
            },
        }
