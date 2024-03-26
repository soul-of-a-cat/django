import django.db.models

import catalog.models
import users.models

__all__ = [
    "Rating",
]


class Rating(django.db.models.Model):
    RATING_CHOICES = [
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
    ]

    user = django.db.models.ForeignKey(
        users.models.User,
        verbose_name="пользователь",
        on_delete=django.db.models.CASCADE,
    )

    item = django.db.models.ForeignKey(
        catalog.models.Item,
        verbose_name="товар",
        on_delete=django.db.models.CASCADE,
    )

    rating = django.db.models.IntegerField(
        verbose_name="оценка",
        choices=RATING_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
