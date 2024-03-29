import django.core.exceptions
import django.core.validators
import django.db.models
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField

import catalog.validators
from core.models import AbstractModel, ImageModel

__all__ = []


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("слаг"),
        help_text="Slug",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = _("тег")
        verbose_name_plural = _("теги")

    def __str__(self):
        return self.name[:15]


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("слаг"),
        help_text="Slug",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name=_("вес"),
        help_text=_("Вес"),
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

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

    def item_list_ratings(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
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
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.tags.field.name}__{Tag.name.field.name}",
                f"{Item.category.field.name}__{Category.name.field.name}",
                f"{Item.main_image.related.name}__"
                f"{ItemMainImage.image.field.name}",
            )
        )

    def items_ratings(self, ratings_items):
        return (
            self.get_queryset()
            .filter(id=ratings_items)
            .only(
                Item.name.field.name,
            )
        )


class Item(AbstractModel):
    objects = ItemManager()

    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name=_("на главной странице"),
        help_text=_("Товары, расположенные на главной странице"),
    )
    text = MDTextField(
        validators=[
            catalog.validators.ValidateMustContain(
                _("превосходно"), _("роскошно")
            ),
            django.core.validators.MinLengthValidator(2),
        ],
        verbose_name=_("текст"),
        help_text=_(
            "Описание должно быть больше, чем из 2х слов "
            "и содержать слова 'превосходно, роскошно'"
        ),
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        null=True,
        verbose_name=_("категория"),
        help_text=_("Выберите категорию"),
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name=_("тег"),
        help_text=_(
            "Удерживайте 'Control' (или 'Command' "
            "на Mac), чтобы выбрать несколько значений"
        ),
    )
    created = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
        help_text=_("Время создания"),
    )
    updated = django.db.models.DateTimeField(
        auto_now=True,
        null=True,
        help_text=_("Время обновления"),
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = _("товар")
        verbose_name_plural = _("товары")

    def __str__(self):
        return self.name[:15]


class ItemMainImage(ImageModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
        help_text=_("Главное изображение"),
    )

    class Meta:
        verbose_name = _("главное изображение")
        verbose_name_plural = _("главные изображения")


class ItemSecondaryImage(ImageModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
        help_text=_("Дополнительное изображение"),
    )

    class Meta:
        verbose_name = _("дополнительное изображение")
        verbose_name_plural = _("дополнительные изображения")
