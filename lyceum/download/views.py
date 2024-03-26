from django.conf import settings
from django.http import FileResponse
from django.views import generic

import catalog.models

__all__ = [
    "DownloadView",
]


class DownloadView(generic.DetailView):
    queryset = catalog.models.ItemMainImage.objects.all()

    def get(self, *args, pk):
        image = self.get_object(self.queryset)
        file_path = f"{settings.MEDIA_ROOT}/{image.image}"
        count = image.image.name.rfind("/") + 1
        name = image.image.name[count::]
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = f"attachment; filename={name}"
        return response
