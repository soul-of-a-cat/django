from django.conf import settings
from django.db import models

__all__ = [
    "Feedback",
    "StatusLog",
    "FeedbackAuthor",
    "FeedbackFile",
    "Status",
]


class Status(models.TextChoices):
    RECEIVED = "Получено"
    PROCESSING = "В обработке"
    ANSWER = "Ответ дан"


class Feedback(models.Model):
    text = models.TextField(
        verbose_name="текст",
        help_text="напишите текст сообщения",
    )
    created_on = models.DateTimeField(
        verbose_name="создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.RECEIVED,
        max_length=11,
        verbose_name="статус",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self) -> str:
        return f"обратная связь ({self.id})"


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    from_status = models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name="с",
        null=True,
    )
    to = models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name="на",
        null=True,
    )

    class Meta:
        verbose_name = "журнал состояния"
        verbose_name_plural = "журнал состояний"

    def __str__(self) -> str:
        return f"состояние ({self.id})"


class FeedbackFile(models.Model):
    def upload_to(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name="обратная связь",
        related_name="files",
        related_query_name="files",
        help_text="файлы",
    )
    file = models.FileField(
        upload_to=upload_to,
    )

    class Meta:
        verbose_name = "файлы обратной связи"
        verbose_name_plural = "файлы обратных связей"


class FeedbackAuthor(models.Model):
    name = models.CharField(
        verbose_name="имя",
        max_length=150,
        help_text="напишите имя",
        null=True,
        blank=True,
    )
    mail = models.EmailField(
        verbose_name="почта",
        help_text="почтовый адрес",
    )
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        related_name="author",
        related_query_name="author",
    )

    class Meta:
        verbose_name = "данные автора"
        verbose_name_plural = "данные авторов"
