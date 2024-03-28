from datetime import timedelta
import random

from django.db.models import Avg, Count
from django.shortcuts import redirect
from django.utils import timezone
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin

import catalog.models
import rating.forms
import rating.models

__all__ = []


class ItemListView(generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published().order_by(
        "category__name"
    )


class ItemDetailView(DetailView, ModelFormMixin):
    template_name = "catalog/item.html"
    model = catalog.models.Item
    form_class = rating.forms.RatingForm

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = rating.models.Rating.objects.filter(
            item=self.get_object(),
        )
        average_rating = ratings.aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]
        num_ratings = ratings.aggregate(num_ratings=Count("rating"))[
            "num_ratings"
        ]

        context["average_rating"] = average_rating
        context["num_ratings"] = num_ratings

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)

        return super().form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            rating_instance = rating.models.Rating.objects.filter(
                user=self.request.user,
                item=self.get_object(),
            ).first()
            initial["item"] = self.get_object().pk
            initial["user"] = self.request.user.id
            if rating_instance:
                initial["rating"] = rating_instance.rating

        return initial

    def form_valid(self, form):
        rating_instance = rating.models.Rating.objects.filter(
            user=self.request.user,
            item=self.object,
        ).first()
        if rating_instance:
            if form.cleaned_data["rating"]:
                rating_instance.rating = form.cleaned_data["rating"]
                rating_instance.save()
            else:
                rating_instance.delete()
        else:
            form.save()

        return redirect("catalog:item-detail", pk=self.object.pk)


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
        items = self.model.objects.friday().order_by(
            f"{catalog.models.Item.category.field.name}__"
            f"{catalog.models.Category.name.field.name}",
            catalog.models.Item.updated.field.name,
        )

        if len(items) > 5:
            return items[-5::]

        return items


class ItemListUnverifiedView(generic.ListView):
    template_name = "catalog/unverified.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        return self.model.objects.unverified().order_by(
            f"{catalog.models.Item.category.field.name}__"
            f"{catalog.models.Category.name.field.name}",
        )
