from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.IntConverter, "pint")

app_name = "catalog"
urlpatterns = [
    path(
        "",
        catalog.views.ItemListView.as_view(),
        name="item-list",
    ),
    re_path(
        r"^re/(?P<pk>[1-9]\d*)/$",
        catalog.views.ItemDetailView.as_view(),
        name="item-detail",
    ),
    path(
        "converter/<pint:pk>/",
        catalog.views.ItemDetailView.as_view(),
        name="item-detail",
    ),
    path(
        "<int:pk>/",
        catalog.views.ItemDetailView.as_view(),
        name="item-detail",
    ),
    path(
        "new/",
        catalog.views.ItemListNewView.as_view(),
        name="new",
    ),
    path(
        "friday/",
        catalog.views.ItemListFridayView.as_view(),
        name="friday",
    ),
    path(
        "unverified/",
        catalog.views.ItemListUnverifiedView.as_view(),
        name="unverified",
    ),
]
