from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.IntConverter, "pint")

urlpatterns = [
    path("", catalog.views.item_list),
    re_path(r"^re/(?P<num>[0-9]+)/", catalog.views.item_detail),
    path("<int:num>/", catalog.views.item_detail),
    path("converter/<pint:num>/", catalog.views.item_detail),
]
