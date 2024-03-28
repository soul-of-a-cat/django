import django.db.models
from django.db.models import Avg, Count, Max, Min, OuterRef, Subquery
from django.shortcuts import render
from django.views import generic

import catalog.models
import rating.models

__all__ = [
    "UserRatingView",
    "ItemListRatingsView",
    "ItemRatingView",
]


class UserRatingView(generic.View):
    def get(self, request):
        items = (
            catalog.models.Item.objects.item_list_ratings().prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.rating.field._related_name,
                    queryset=rating.models.Rating.objects.filter(
                        user=request.user,
                    ),
                )
            )
        )

        vals_rating = items.aggregate(
            avg_rating=Avg("rating"),
            num_ratings=Count("rating"),
            max_rating=Max("rating"),
            min_rating=Min("rating"),
        )

        rating_items = {}

        if vals_rating["num_ratings"] > 0:
            max_rating_item = items.filter(
                rating=vals_rating["max_rating"]
            ).first()
            min_rating_item = items.filter(
                rating=vals_rating["min_rating"]
            ).first()

            rating_items = {
                "Самый лучший товар": max_rating_item,
                "Самый плохой товар": min_rating_item,
            }

        return render(
            request,
            "statistics/user_ratings.html",
            {
                "items": rating_items,
                "count_ratings": vals_rating["num_ratings"],
                "average_rating": vals_rating["avg_rating"],
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
        last_max_rating_subquery = (
            rating.models.Rating.objects.filter(item=OuterRef("id"))
            .order_by("-rating")
            .values("user__username")[:1]
        )
        last_min_rating_subquery = (
            rating.models.Rating.objects.filter(item=OuterRef("id"))
            .order_by("rating")
            .values("user__username")[:1]
        )

        items = (
            catalog.models.Item.objects.prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.rating.field._related_name,
                    queryset=rating.models.Rating.objects.only(
                        "user__username",
                        rating.models.Rating.rating.field.name,
                    ),
                ),
            )
            .filter(
                id=django.db.models.F("rating__item"),
            )
            .annotate(
                avg_rating=Avg("rating__rating"),
                num_ratings=Count("rating__rating"),
                max_rating_user=Subquery(last_max_rating_subquery),
                min_rating_user=Subquery(last_min_rating_subquery),
            )
        )

        context = {}

        for item in items:
            item_context = {}

            item_context["Среднее оценок"] = item.avg_rating
            item_context["Количество оценок"] = item.num_ratings

            item_context["Пользователь, поставивший максимальную оценку"] = (
                item.max_rating_user
            )
            item_context["Пользователь, поставивший минимальную оценку"] = (
                item.min_rating_user
            )

            context[item.name] = item_context

        return render(
            request,
            "statistics/items_rating.html",
            {
                "items": context,
            },
        )
