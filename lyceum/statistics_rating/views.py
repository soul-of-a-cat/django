import django.db.models
from django.db.models import Avg, Count, Max, Min
from django.shortcuts import render
from django.views import generic

import catalog.models
import rating.models
import users.models

__all__ = [
    "UserRatingView",
    "ItemListRatingsView",
    "ItemRatingView",
]


class UserRatingView(generic.View):
    def get(self, request):
        ratings = rating.models.Rating.objects.filter(
            user=request.user.id,
        ).only(
            rating.models.Rating.rating.field.name,
            rating.models.Rating.user.field.name,
            rating.models.Rating.item.field.name,
            rating.models.Rating.updated.field.name,
        )

        average_rating = ratings.aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]
        count_ratings = ratings.aggregate(num_ratings=Count("rating"))[
            "num_ratings"
        ]

        rating_items = {}

        if count_ratings > 0:
            mxr = ratings.aggregate(max_rating=Max("rating"))["max_rating"]
            mnr = ratings.aggregate(min_rating=Min("rating"))["min_rating"]

            max_rating = ratings.filter(rating=mxr).latest("updated")
            min_rating = ratings.filter(rating=mnr).latest("updated")

            items = catalog.models.Item.objects.item_list_ratings()

            max_rating_item = items.get(id=max_rating.item.id)
            min_rating_item = items.get(id=min_rating.item.id)

            rating_items = {
                "Самый лучший товар": max_rating_item,
                "Самый плохой товар": min_rating_item,
            }

        return render(
            request,
            "statistics/user_ratings.html",
            {
                "items": rating_items,
                "count_ratings": count_ratings,
                "average_rating": average_rating,
            },
        )


class ItemListRatingsView(generic.View):
    def get(self, request):
        items = (
            catalog.models.Item.objects.item_list_ratings()
            .prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.rating.field._related_name,
                    queryset=rating.models.Rating.objects.filter(
                        user=request.user.id,
                    ),
                ),
            )
            .filter(
                id=django.db.models.F("rating__item"),
            )
        )
        return render(
            request,
            "statistics/item_list_ratings.html",
            {
                "items": items,
            },
        )


class ItemRatingView(generic.View):
    def get(self, request):
        items = (
            catalog.models.Item.objects.all()
            .prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.rating.field._related_name,
                    queryset=rating.models.Rating.objects.all(),
                ),
            )
            .filter(
                id=django.db.models.F("rating__item"),
            )
            .only(
                catalog.models.Item.name.field.name,
            )
        )

        context = {}

        for item in items:
            item_context = {}

            ratings = rating.models.Rating.objects.filter(
                item=item.id,
            ).only(
                rating.models.Rating.rating.field.name,
                rating.models.Rating.user.field.name,
                rating.models.Rating.item.field.name,
            )

            item_context["Среднее оценок"] = ratings.aggregate(
                avg_rating=Avg("rating")
            )["avg_rating"]
            item_context["Количество оценок"] = ratings.aggregate(
                num_ratings=Count("rating")
            )["num_ratings"]

            mxr = ratings.aggregate(max_rating=Max("rating"))["max_rating"]
            mnr = ratings.aggregate(min_rating=Min("rating"))["min_rating"]

            max_rating = ratings.filter(rating=mxr).latest("updated")
            min_rating = ratings.filter(rating=mnr).latest("updated")

            user = users.models.User.objects.all().only(
                users.models.User.username.field.name,
            )

            item_context["Пользователь, поставивший максимальную оценку"] = (
                user.get(id=max_rating.user.id)
            )
            item_context["Пользователь, поставивший минимальную оценку"] = (
                user.get(id=min_rating.user.id)
            )

            context[item.name] = item_context

        return render(
            request,
            "statistics/items_rating.html",
            {
                "items": context,
            },
        )
