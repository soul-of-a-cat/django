import django.db.models
from django.utils.translation import gettext_lazy as _

import catalog.models
import users.models

__all__ = []


class Rating(django.db.models.Model):
    RATING_CHOICES = [
        (1, _("Ненависть")),
        (2, _("Неприязнь")),
        (3, _("Нейтрально")),
        (4, _("Обожание")),
        (5, _("Любовь")),
    ]

    user = django.db.models.ForeignKey(
        users.models.User,
        verbose_name=_("пользователь"),
        on_delete=django.db.models.CASCADE,
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        verbose_name=_("товар"),
        on_delete=django.db.models.CASCADE,
        related_name="rating",
        related_query_name="rating",
    )
    rating = django.db.models.IntegerField(
        verbose_name=_("оценка"),
        choices=RATING_CHOICES,
        null=True,
        blank=True,
    )
    updated = django.db.models.DateTimeField(
        auto_now=True,
        null=True,
    )

    class Meta:
        ordering = ("-updated",)
        default_related_name = "rating"
        verbose_name = _("оценка")
        verbose_name_plural = _("оценки")
