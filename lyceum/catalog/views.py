from datetime import date, timedelta
import random

from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin

import catalog.models
import rating.forms
import rating.models

__all__ = [
    "item_list",
    "ItemDetailView",
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


class ItemDetailView(DetailView, ModelFormMixin):
    template_name = "catalog/item.html"
    model = catalog.models.Item
    form_class = rating.forms.RatingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = rating.models.Rating.objects.filter(
            item=self.get_object(),
        )
        average_rating = ratings.aggregate(avg_rating=Avg("rating"))[
            "avg_rating",
        ]
        num_ratings = ratings.aggregate(num_ratings=Count("rating"))[
            "num_ratings",
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


def new(request):
    template = "catalog/new.html"
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    items_all = list(
        catalog.models.Item.objects.new(start_date, end_date),
    )

    if len(items_all) > 5:
        items = random.sample(items_all, 5)
    else:
        items = items_all

    items = sorted(items, key=lambda x: x.category.name)

    context = {"items": items}

    return render(
        request,
        template,
        context,
    )


def friday(request):
    template = "catalog/friday.html"

    items = catalog.models.Item.objects.friday()

    items = sorted(items, key=lambda x: (x.category.name, x.updated))

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

    items = catalog.models.Item.objects.unverified()

    items = sorted(items, key=lambda x: x.category.name)

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
