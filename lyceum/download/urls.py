from django.urls import path

import download.views

app_name = "download"
urlpatterns = [
    path(
        "<int:pk>/",
        download.views.DownloadView.as_view(),
        name="download-main-image",
    ),
]
