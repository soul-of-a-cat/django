from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.IntConverter, "pint")

app_name = "catalog"
urlpatterns = [
    path(
        "",
        catalog.views.item_list,
        name="item_list",
    ),
    re_path(
        r"^re/(?P<num>[1-9]\d*)/$",
        catalog.views.item_detail,
        name="item_detail",
    ),
    path(
        "converter/<pint:num>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    path(
        "<int:num>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    path(
        "new/",
        catalog.views.new,
        name="new",
    ),
    path(
        "friday/",
        catalog.views.friday,
        name="friday",
    ),
    path(
        "unverified/",
        catalog.views.unverified,
        name="unverified",
    ),
]
