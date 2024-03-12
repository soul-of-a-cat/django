from datetime import date, timedelta
import random

import django.db.models
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = [
    "item_list",
    "item_detail",
    "friday",
    "new",
    "unverified",
]


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("category__name")

    context = {
        "items": items,
    }
    return render(
        request,
        template,
        context,
    )


def item_detail(request, num):
    template = "catalog/item.html"
    item = get_object_or_404(
        catalog.models.Item.objects.item_detail(),
        id=num,
    )

    context = {
        "item": item,
    }
    return render(
        request,
        template,
        context,
    )


def new(request):
    template = "catalog/new.html"
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    items_all = list(
        catalog.models.Item.objects.published()
        .filter(created__range=[start_date, end_date])
        .order_by("category__name"),
    )

    if len(items_all) > 5:
        items = random.sample(items_all, 5)
        items = sorted(items, key=lambda x: x.category.name)
    else:
        items = items_all

    context = {"items": items}

    return render(
        request,
        template,
        context,
    )


def friday(request):
    template = "catalog/friday.html"

    items = (
        catalog.models.Item.objects.published()
        .filter(updated__iso_week_day=5)
        .order_by("category__name", "updated")
    )

    if len(items) > 5:
        context = {
            "items": items[-5::],
        }
    elif 0 < len(items) <= 5:
        context = {
            "items": items,
        }
    else:
        context = {}

    return render(
        request,
        template,
        context,
    )


def unverified(request):
    template = "catalog/unverified.html"

    items = (
        catalog.models.Item.objects.published()
        .filter(created=django.db.models.F("updated"))
        .order_by("category__name")
    )

    if len(items) > 0:
        context = {
            "items": items,
        }
    else:
        context = {}

    return render(
        request,
        template,
        context,
    )
