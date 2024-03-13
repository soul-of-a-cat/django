from django.contrib.auth.models import User
from django.db import models

__all__ = [
    "Feedback",
]


class Feedback(models.Model):
    class Status(models.IntegerChoices):
        RECEIVED = 0, "Получено"
        PROCESSING = 1, "В обработке"
        ANSWER = 2, "Ответ дан"

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
        choices=Status.choices,
        default=Status.RECEIVED,
    )

    class Meta:
        app_label = "feedback"

    def __str__(self):
        return self.text[:10]


class StatusLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="создано",
        help_text="Дата и время создания",
        auto_now_add=True,
        null=True,
    )
