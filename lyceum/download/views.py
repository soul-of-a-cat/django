from django.http import FileResponse
from django.shortcuts import get_object_or_404

import catalog.models

__all__ = [
    "download_main_image",
]


def download_main_image(request, main_image_id):
    image = get_object_or_404(catalog.models.ItemMainImage, pk=main_image_id)
    file_path = f".{image.image.url}"
    count = image.image.name.rfind("/") + 1
    name = image.image.name[count::]
    response = FileResponse(open(file_path, "rb"))
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = f"attachment; filename='{name}'"
    return response
