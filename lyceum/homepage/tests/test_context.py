from django.db.models import QuerySet
from django.test import Client, TestCase
from django.urls import reverse

import catalog.models

__all__ = [
    "ContextTest",
]


class ContextTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="Тестовая неопубликованная категория",
            slug="uppublished_category",
            weight=100,
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Опубликованный тег",
            slug="published_tag",
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Неопубликованный тег",
            slug="unpublished_tag",
        )

        cls.unpublished_item = catalog.models.Item(
            name="Неопубликованный товар",
            category=cls.published_category,
            text="превосходно",
            is_published=False,
        )
        cls.published_item = catalog.models.Item(
            name="Опубликованный товар",
            category=cls.published_category,
            text="превосходно",
            is_published=True,
            is_on_main=True,
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item.clean()
        cls.published_item.save()
        cls.unpublished_item.clean()
        cls.unpublished_item.save()

        cls.published_item.tags.add(cls.published_tag.id)
        cls.published_item.tags.add(cls.unpublished_tag.id)

    def test_homepage_show_correct_context(self):
        response = Client().get(reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_context_items_type(self):
        response = Client().get(reverse("homepage:home"))
        items = response.context["items"]
        expected_type = QuerySet

        self.assertIsInstance(items, expected_type)

    def test_context_items_field(self):
        response = Client().get(reverse("homepage:home"))
        items = response.context["items"].first().__dict__
        tags = items["_prefetched_objects_cache"]["tags"].first().__dict__
        need_fields = [
            "name",
            "text",
            "category_id",
        ]
        unnecessary_fields = [
            "is_published",
            "category_is_published",
            "category_slug",
        ]

        for field in need_fields:
            self.assertIn(
                field,
                items,
                f"{field} not expected in context items",
            )

        self.assertIn("name", tags)

        for field in unnecessary_fields:
            self.assertNotIn(
                field,
                items,
                f"{field} was found in context items",
            )

        self.assertNotIn("is_published", tags)
        self.assertNotIn("slug", tags)
