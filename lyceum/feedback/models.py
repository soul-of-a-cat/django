from django.contrib.auth.models import User
from django.db import models

__all__ = [
    "Feedback",
]


class Status(models.TextChoices):
    RECEIVED = "Получено"
    PROCESSING = "В обработке"
    ANSWER = "Ответ дан"


class Feedback(models.Model):
    name = models.CharField(
        "имя",
        help_text="Напишите своё имя",
        max_length=100,
        null=True,
        blank=True,
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
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self):
        return self.text[:10]


class StatusLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="пользователь",
    )
    timestamp = models.DateTimeField(
        verbose_name="создано",
        help_text="Дата и время создания",
        auto_now_add=True,
        null=True,
    )
    from_status = models.CharField(
        verbose_name="status",
        help_text="Статус",
        max_length=100,
        choices=Status.choices,
        null=True,
        db_column="from",
    )
    to_status = models.CharField(
        verbose_name="status",
        help_text="Статус",
        max_length=100,
        choices=Status.choices,
        null=True,
        db_column="to",
    )
