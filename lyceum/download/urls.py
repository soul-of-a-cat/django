from django.urls import path
import Download.views

app_name = "download"
urlpatterns = [
    path(
        "<int:main_image_id>/",
        Download.views.download_main_image,
        name="download_main_image",
    ),
]
