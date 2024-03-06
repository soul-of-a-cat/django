import django.db.models
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = ["item_list", "item_detail"]


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("category__name")
    context = {"items": items}
    return render(
        request,
        template,
        context,
    )


def item_detail(request, num):
    template = "catalog/item.html"
    item = get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True)
        .select_related("category")
        .select_related("main_image")
        .filter(category__is_published=True)
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .prefetch_related(
            django.db.models.Prefetch(
                "images",
                queryset=catalog.models.ItemSecondaryImage.objects.only(
                    "image",
                ),
            ),
        )
        .only("name", "category__name", "text", "main_image__image"),
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
