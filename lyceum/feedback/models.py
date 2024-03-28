from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = []


class Status(models.TextChoices):
    RECEIVED = _("Получено")
    PROCESSING = _("В обработке")
    ANSWER = _("Ответ дан")


class Feedback(models.Model):
    text = models.TextField(
        verbose_name=_("текст"),
        help_text=_("напишите текст сообщения"),
    )
    created_on = models.DateTimeField(
        verbose_name=_("создано"),
        help_text=_("дата и время создания"),
        auto_now_add=True,
        null=True,
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.RECEIVED,
        max_length=11,
        verbose_name=_("статус"),
        help_text=_("Статус"),
    )

    class Meta:
        verbose_name = _("обратная связь")
        verbose_name_plural = _("обратные связи")

    def __str__(self) -> str:
        return _(f"обратная связь ({self.id})")


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Пользователь"),
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Обратная связь"),
    )
    timestamp = models.DateTimeField(
        verbose_name=_("создано"),
        help_text=_("дата и время создания"),
        auto_now_add=True,
        null=True,
    )
    from_status = models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name=_("с"),
        null=True,
        help_text=_("с"),
    )
    to = models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name=_("на"),
        null=True,
        help_text=_("на"),
    )

    class Meta:
        verbose_name = _("журнал состояния")
        verbose_name_plural = _("журнал состояний")

    def __str__(self) -> str:
        return _(f"состояние ({self.id})")


class FeedbackFile(models.Model):
    def upload_to(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name=_("обратная связь"),
        related_name="files",
        related_query_name="files",
        help_text=_("файлы"),
    )
    file = models.FileField(
        upload_to=upload_to,
        help_text=_("Файлы"),
    )

    class Meta:
        verbose_name = _("файлы обратной связи")
        verbose_name_plural = _("файлы обратных связей")


class FeedbackAuthor(models.Model):
    name = models.CharField(
        verbose_name=_("имя"),
        max_length=150,
        help_text=_("напишите имя"),
        null=True,
        blank=True,
    )
    mail = models.EmailField(
        verbose_name=_("почта"),
        help_text=_("почтовый адрес"),
    )
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        related_name="author",
        related_query_name="author",
        help_text=_("Обратная связь"),
    )

    class Meta:
        verbose_name = _("данные автора")
        verbose_name_plural = _("данные авторов")
