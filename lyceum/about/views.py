from django.http import HttpResponse
from http import HTTPStatus


def description(request):
    return HttpResponse(
        "О проекте",
        status=HTTPStatus.OK,
    )
