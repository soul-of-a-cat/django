from datetime import timedelta
import random

from django.utils import timezone
from django.views import generic

import catalog.models

__all__ = [
    "ItemListView",
    "ItemDetailView",
    "ItemListNewView",
    "ItemListFridayView",
    "ItemListUnverifiedView",
]


class ItemListView(generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published().order_by(
        "category__name"
    )


class ItemDetailView(generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.item_detail()


class ItemListNewView(generic.ListView):
    template_name = "catalog/new.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)

        items_all = list(
            self.model.objects.new(start_date, end_date),
        )

        if len(items_all) > 5:
            items = random.sample(items_all, 5)
        else:
            items = items_all

        return sorted(items, key=lambda x: x.category.name)


class ItemListFridayView(generic.ListView):
    template_name = "catalog/friday.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        items = self.model.objects.friday()

        items = sorted(items, key=lambda x: (x.category.name, x.updated))

        if len(items) > 5:
            return items[-5::]

        return items


class ItemListUnverifiedView(generic.ListView):
    template_name = "catalog/unverified.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        return sorted(
            self.model.objects.unverified(), key=lambda x: x.category.name
        )
