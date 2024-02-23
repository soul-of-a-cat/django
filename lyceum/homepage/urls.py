from django.urls import path

import homepage.views

urlpatterns = [
    path("", homepage.views.home, name="Главная"),
    path("coffee/", homepage.views.coffee, name="А где же мой кофе?"),
]
