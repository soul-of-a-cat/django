from pathlib import Path
import re
import uuid

import django.core.exceptions
import django.db.models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import sorl
import transliterate

__all__ = []

ONLY_LETTERS_REGEX = re.compile(r"\W")


def get_path_image(instance, filename):
    ext = filename.split(".")[-1]
    return f"catalog/{uuid.uuid4()}.{ext}"


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name=_("опубликовано"),
        help_text=_("Опубликовано"),
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name=_("название"),
        help_text=_("max 150 символов"),
        unique=True,
    )

    normalized_name = django.db.models.CharField(
        unique=True,
        editable=False,
        max_length=150,
        null=True,
        verbose_name=_("нормализованное название"),
        help_text=_("Нормализованное название элемента"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.normalized_name = self._generate_normalized_name()
        super().save(*args, **kwargs)

    def clean(self):
        self.normalized_name = self._generate_normalized_name()
        if (
            type(self)
            .objects.filter(normalized_name=self.normalized_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                _("Уже есть такой же элемент"),
            )

    def _generate_normalized_name(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub(
            "",
            transliterated,
        )


class ImageModel(django.db.models.Model):
    image = sorl.thumbnail.ImageField(
        upload_to=get_path_image,
        verbose_name=_("изображение"),
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_413x413(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "413x413",
            crop="center",
            quality=51,
        )

    def get_image_108x108(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "108x108",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            tag = f'<img src="{self.get_image_300x300().url}">'
            return mark_safe(tag)

        return _("изображение отсутствует")

    image_tmb.short_description = _("превью")
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"

    class Meta:
        abstract = True

    def __str__(self):
        return Path(self.image.path).stem
