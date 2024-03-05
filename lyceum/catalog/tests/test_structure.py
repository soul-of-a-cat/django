from http import HTTPStatus
import itertools

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
import parameterized

import catalog.models

__all__ = [
    "StaticUrlTests",
    "DBItemTests",
    "DBTagTests",
    "DBCategoryTests",
    "DBNormalizeNameTests",
]


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        url = reverse("catalog:item_list")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class DBItemTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
            slug="Test",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
            slug="Test",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходно"),
            ("test", "роскошно"),
            ("test", "Я превосходно"),
            ("test", "превосходно Я"),
            ("test", "превосходно роскошно"),
            ("test", "роскошно!"),
            ("test", "!роскошно"),
            ("test", "!роскошно"),
            ("test", "роскошно©"),
        ],
    )
    def test_add_item_no_error(self, name, text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=text,
            category=self.category,
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)
        self.item.full_clean()
        self.item.save()
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
            msg="no add validate item",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходноН"),
            ("test", "превНосходно"),
            ("test", "Нпревосходно"),
            ("test", "Я превосх%одно"),
            ("test", "превосходнороскошно"),
            ("test" * 38, "превосходно"),
        ],
    )
    def test_add_item_error(self, name, text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=text,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg="add no validate item",
        )


class DBTagTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs"),
            ("test", "1abs2"),
            ("test", "a12bs"),
            ("test", "ABS"),
            ("test", "-abs-"),
            ("test", "_abs_"),
        ],
    )
    def test_add_tag_no_error(self, name, slug):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
            msg="no add validate item",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "Я"),
            ("test", "Яabs"),
            ("test", "Я abs"),
            ("test", "aЯbs"),
            ("test", "absЯ"),
            ("test", "abs Я"),
            ("test", "*abs*"),
            ("test", "a*bs"),
            ("test" * 38, "abs"),
            ("test", "abs" * 67),
        ],
    )
    def test_add_tag_error(self, name, slug):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        with self.assertRaises(ValidationError):
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg="add no validate item",
        )


class DBCategoryTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", 1),
            ("test", "1abs2", 1),
            ("test", "a12bs", 1),
            ("test", "ABS", 1),
            ("test", "-abs-", 1),
            ("test", "_abs_", 1),
            ("test", "_abs_", 32767),
        ],
    )
    def test_add_category_no_error(self, name, slug, weight):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
            msg="no add validate item",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "Я", 1),
            ("test", "Яabs", 1),
            ("test", "Я abs", 1),
            ("test", "aЯbs", 1),
            ("test", "absЯ", 1),
            ("test", "abs Я", 1),
            ("test", "*abs*", 1),
            ("test", "a*bs", 1),
            ("test" * 38, "abs", 1),
            ("test", "abs" * 67, 1),
            ("test", "abs", 32768),
            ("test", "abs", 0),
            ("test", "abs", -1),
        ],
    )
    def test_add_category_error(self, name, slug, weight):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        with self.assertRaises(ValidationError):
            self.category.full_clean()
            self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg="add no validate item",
        )


class DBNormalizeNameTests(TestCase):
    @parameterized.parameterized.expand(
        (
            (x[0], x[1])
            for x in itertools.product(
                [
                    ("test", "1"),
                ],
                [
                    ("test test", "2"),
                    ("itfaketest", "2"),
                    ("test, test", "2"),
                    ("test!test", "2"),
                    ("testt", "2"),
                ],
            )
        ),
    )
    def test_add_item_normalize_name_no_error(self, data1, data2):
        self.tag = catalog.models.Tag(
            name=data1[0],
            slug=data1[1],
        )
        self.tag.full_clean()
        self.tag.save()
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=data2[0],
            slug=data2[1],
        )
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
            msg="no add validate item",
        )

    @parameterized.parameterized.expand(
        (
            (x[0], x[1])
            for x in itertools.product(
                [
                    ("test", "1"),
                ],
                [
                    ("test!", "2"),
                    ("!test", "2"),
                    ("!test!", "2"),
                    (" test ", "2"),
                    ("test,", "2"),
                    (".test", "2"),
                    ("te st", "2"),
                ],
            )
        ),
    )
    def test_add_item_normalize_name_error(self, data1, data2):
        self.tag = catalog.models.Tag(
            name=data1[0],
            slug=data1[1],
        )
        self.tag.full_clean()
        self.tag.save()
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=data2[0],
            slug=data2[1],
        )
        with self.assertRaises(ValidationError):
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg="add no validate item",
        )
