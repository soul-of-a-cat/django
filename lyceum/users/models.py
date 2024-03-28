import sys

import django.contrib.auth.models
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import sorl.thumbnail


__all__ = [
    "Profile",
    "User",
    "UserManager",
]

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    AuthUser._meta.get_field("email")._unique = True


@receiver(post_save, sender=AuthUser)
def create_superuser_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Profile.objects.create(user=instance)


class Profile(models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    birthday = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
        help_text="Введите дату рождения пользователя",
    )
    coffee_count = models.PositiveIntegerField(
        "Сколько раз пользователь пил кофе",
        default=0,
        help_text="Количество переходов по /coffee/",
    )
    attempts_count = models.PositiveIntegerField(
        "Попытки входа",
        default=0,
    )
    block_date = models.DateTimeField(
        "Дата блокировки",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        "аватарка",
        help_text="Загрузите автарку",
        upload_to=image_path,
        null=True,
        blank=True,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
    }
    DOTS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self) -> models.query.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                User.profile.related.name,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        normalize_email = self.normalize_email(mail)
        return self.active().get(email=normalize_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email_name, _ = email_name.split("+", 1)

            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = "@".join([email_name, domain_part.lower()])

        return email


class User(AuthUser):
    objects = UserManager()

    class Meta:
        proxy = True
