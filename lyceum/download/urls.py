from django.urls import path

import download.views

app_name = "download"
urlpatterns = [
    path(
        "<int:main_image_id>/",
        download.views.download_main_image,
        name="download-main-image",
    ),
]
