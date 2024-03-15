from pathlib import Path
import re
import uuid

import django.db.models
from django.utils.safestring import mark_safe
from slugify import slugify
import sorl

__all__ = [
    "AbstractModel",
    "BaseModel",
    "normalize_name",
]


def get_path_image(instance, filename):
    ext = filename.split(".")[-1]
    return f"catalog/{uuid.uuid4()}.{ext}"


def normalize_name(name):
    words = re.findall("[0-9а-яёa-z]+", name.lower())
    return slugify("".join(words))


class BaseModel(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        unique=True,
        editable=False,
        max_length=150,
        validators=[
            django.core.validators.MaxLengthValidator(150),
        ],
        null=True,
    )

    def clean(self) -> None:
        normalized = normalize_name(self.name)
        existing = self.__class__.objects.filter(
            normalized_name=normalized,
        )
        if existing:
            raise django.core.exceptions.ValidationError(
                {
                    self.__class__.name.field.name: "Такое имя уже имеется",
                },
            )

        self.normalized_name = normalized

    class Meta:
        abstract = True


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
        unique=True,
    )

    class Meta:
        abstract = True


class ImageModel(django.db.models.Model):
    image = sorl.thumbnail.ImageField(
        upload_to=get_path_image,
        verbose_name="изображение",
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

        return "изображение отсутствует"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"

    class Meta:
        abstract = True

    def __str__(self):
        return Path(self.image.path).stem
