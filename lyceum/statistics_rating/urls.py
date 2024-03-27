from django.urls import path

import statistics_rating.views

app_name = "statistics_rating"
urlpatterns = [
    path(
        "user/",
        statistics_rating.views.UserRatingView.as_view(),
        name="user-rating",
    ),
    path(
        "item_list/",
        statistics_rating.views.ItemListRatingsView.as_view(),
        name="item-list-rating",
    ),
    path(
        "item/",
        statistics_rating.views.ItemRatingView.as_view(),
        name="items-rating",
    ),
]
