from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.IntConverter, "pint")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    re_path(r"^re/(?P<num>[0-9]+)/", views.number, name="renumber"),
    path("<int:item_id>/", views.item_detail, name="item_detail"),
    path("converter/<pint:num>/", views.converter, name="converter"),
]
