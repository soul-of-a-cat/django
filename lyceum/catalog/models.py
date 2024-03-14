from django import forms
import django.core.exceptions
import django.core.validators
import django.db.models
from mdeditor.fields import MDTextField

import catalog.validators
from core.models import AbstractModel, BaseModel, ImageModel

__all__ = [
    "Category",
    "Item",
    "Tag",
    "ItemManager",
    "ItemSecondaryImage",
    "ItemMainImage",
]


class Tag(AbstractModel, BaseModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(AbstractModel, BaseModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name="вес",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


class ItemManager(django.db.models.Manager):
    def published(self):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__{ItemMainImage.item.field.name}",
        )

    def on_main(self):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                is_on_main=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__"
            f"{ItemMainImage.item.field.name}",
        )

    def item_detail(self):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
                django.db.models.Prefetch(
                    Item.images.field._related_name,
                    queryset=ItemSecondaryImage.objects.all(),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.main_image.related.name}__"
            f"{ItemMainImage.item.field.name}",
            f"{Item.images.field._related_name}__"
            f"{ItemSecondaryImage.item.field.name}",
        )

    def new(self, start, end):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                created__range=[start, end],
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__{ItemMainImage.item.field.name}",
        )

    def friday(self):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                updated__iso_week_day=5,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            Item.updated.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__{ItemMainImage.item.field.name}",
        )

    def unverified(self):
        items = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                created=django.db.models.F("updated"),
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return items.only(
            Item.name.field.name,
            Item.text.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__{ItemMainImage.item.field.name}",
        )


class Item(AbstractModel):
    objects = ItemManager()

    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name="на главной странице",
    )
    text = MDTextField(
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
            django.core.validators.MinLengthValidator(2),
        ],
        verbose_name="текст",
        help_text="Описание должно быть больше, чем из 2х слов "
        "и содержать слова 'превосходно, роскошно'",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        null=True,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="тег",
        help_text="Удерживайте 'Control' (или 'Command' "
        "на Mac), чтобы выбрать несколько значений",
    )
    created = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated = django.db.models.DateTimeField(
        auto_now=True,
        null=True,
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.text[:15]


class ItemMainImage(ImageModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemSecondaryImage(ImageModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"
