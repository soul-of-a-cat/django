import sys
import uuid
from pathlib import Path
from typing import cast, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


__all__ = []

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True


def get_path_image(instance, filename):
    ext = Path(filename).suffix
    return f"users/{uuid.uuid4()}{ext}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
        help_text="Введите дату рождения пользователя",
    )
    coffee_count = models.PositiveIntegerField(
        "Сколько раз пользователь пил кофе",
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Количество переходов по /coffee/",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        "аватарка",
        help_text="Загрузите автарку",
        upload_to=get_path_image,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


class UserManager(models.Manager):
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
        return cast(Optional[User], self.get_queryset().get(email=mail))

    def normalize_email(self, mail):
        return mail


class User(get_user_model()):
    objects = UserManager()

    class Meta:
        proxy = True
