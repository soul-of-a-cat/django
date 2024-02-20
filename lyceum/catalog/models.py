from Core.models import AbstractModel
import django.core.exceptions
import django.core.validators
import django.db.models


def perfect_in_text_validator(value):
    value = value.lower()
    if "превосходно" not in value and "роскошно" not in value:
        raise django.core.exceptions.ValidationError(
            "Нет слово превосходно или роскошно в тексте",
        )


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name[:15]


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(0),
        ],
        verbose_name="Вес",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:15]


class Item(AbstractModel):
    text = django.db.models.TextField(
        validators=[
            perfect_in_text_validator,
            django.core.validators.MinLengthValidator(2),
        ],
        verbose_name="Текст",
        help_text="Описание должно быть больше, чем из 2х слов "
        "и содержать слова 'превосходно, роскошно'",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        null=True,
        verbose_name="Категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="Тег",
        help_text="Удерживайте 'Control' (или 'Command' "
        "на Mac), чтобы выбрать несколько значений",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.text[:15]
