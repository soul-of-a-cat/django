from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.IntConverter, "pint")

urlpatterns = [
    path("", views.item_list),
    re_path(r"^re/(?P<num>[0-9]+)/", views.item_detail),
    path("<int:num>/", views.item_detail),
    path("converter/<pint:num>/", views.item_detail),
]
