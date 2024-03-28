import django.db.models
from django.db.models import Avg, Count, OuterRef, Subquery
from django.shortcuts import render
from django.views import generic

import catalog.models
from rating.models import Rating
import users.models

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
                    queryset=Rating.objects.filter(
                        user=request.user,
                    ),
                )
            )
        )

        vals_rating = items.aggregate(
            avg_rating=Avg("rating__rating"),
            num_ratings=Count("rating__rating"),
        )

        rating_items = {}

        if vals_rating["num_ratings"] > 0:
            max_rating_item = items.order_by(
                f"-{catalog.models.Item.rating.field._related_name}__"
                f"{Rating.rating.field.name}"
            ).first()
            min_rating_item = items.order_by(
                f"{catalog.models.Item.rating.field._related_name}__"
                f"{Rating.rating.field.name}"
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
                    queryset=Rating.objects.filter(
                        user=request.user.id,
                    ),
                ),
            )
            .filter(
                id=django.db.models.F(
                    f"{catalog.models.Item.rating.field._related_name}__"
                    f"{Rating.item.field.name}"
                ),
            )
            .order_by(
                f"-{catalog.models.Item.rating.field._related_name}__"
                f"{Rating.rating.field.name}"
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
        last_max_rating_user_subquery = (
            Rating.objects.filter(item=OuterRef("id"))
            .order_by(f"-{Rating.rating.field.name}")
            .values(
                f"{Rating.user.field.name}__"
                f"{users.models.User.username.field.name}"
            )[:1]
        )
        last_min_rating_user_subquery = (
            Rating.objects.filter(item=OuterRef("id"))
            .order_by(Rating.rating.field.name)
            .values(
                f"{Rating.user.field.name}__"
                f"{users.models.User.username.field.name}"
            )[:1]
        )

        items = (
            catalog.models.Item.objects.prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.rating.field._related_name,
                    queryset=Rating.objects.only(
                        f"{Rating.user.field.name}__"
                        f"{users.models.User.username.field.name}",
                        Rating.rating.field.name,
                    ),
                ),
            )
            .filter(
                id=django.db.models.F(
                    f"{catalog.models.Item.rating.field._related_name}__"
                    f"{Rating.item.field.name}"
                ),
            )
            .annotate(
                avg_rating=Avg(
                    f"{catalog.models.Item.rating.field._related_name}__"
                    f"{Rating.rating.field.name}"
                ),
                num_ratings=Count(
                    f"{catalog.models.Item.rating.field._related_name}__"
                    f"{Rating.rating.field.name}"
                ),
                max_rating_user=Subquery(last_max_rating_user_subquery),
                min_rating_user=Subquery(last_min_rating_user_subquery),
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
