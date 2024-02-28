from django.urls import path

import homepage.views

app_name = "homepage"
urlpatterns = [
    path("", homepage.views.home, name="home"),
    path("coffee/", homepage.views.coffee, name="coffee"),
]
