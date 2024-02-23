from django.http import HttpResponse
from http import HTTPStatus


def item_list(request):
    return HttpResponse(
        "Список элементов",
        status=HTTPStatus.OK,
    )


def item_detail(request, num):
    return HttpResponse(
        "Подробно элемент",
        status=HTTPStatus.OK,
    )
