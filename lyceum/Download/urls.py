from django.urls import path

import Download.views

app_name = "Download"
urlpatterns = [
    path(
        "<int:main_image_id>/",
        Download.views.download_main_image,
        name="download_main_image",
    ),
]
