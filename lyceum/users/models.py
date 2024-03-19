from pathlib import Path
import uuid

from django.conf import settings
from django.db import models


__all__ = [
    "Profile",
]


def get_path_image(instance, filename):
    ext = Path(filename).suffix
    return f"users/{uuid.uuid4()}{ext}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="пользователь",
        help_text="укажите пользователя",
        on_delete=models.CASCADE,
    )
    birthday = models.DateField(
        "день рождения",
        help_text="укажите дату рождения",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        "аватарка",
        help_text="загрузите автарку",
        upload_to=get_path_image,
    )
    coffee_count = models.PositiveIntegerField(
        "количество переходов по /coffee/",
        help_text="сколько раз пользователь пытался сварить кофе ",
        default=0,
    )

    class Meta:
        verbose_name = "дополнительное поле пользователя"
        verbose_name_plural = "дополнительные поля пользователей"
