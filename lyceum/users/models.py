from pathlib import Path
from typing import cast
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
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


class UserProxyManager(models.Manager):
    def get_queryset(self) -> models.query.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                User.profile.related.name,
            )
        )

    def active(self) -> models.query.QuerySet:
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail: str) -> "User | None":
        return cast(User | None, self.get_queryset().get(email=mail))


class UserProxy(get_user_model()):
    objects = UserProxyManager()

    class Meta:
        proxy = True
