from django.db import models

__all__ = [
    "Feedback",
]


class Feedback(models.Model):
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

    class Meta:
        app_label = "feedback"

    def __str__(self):
        return self.text[:10]
