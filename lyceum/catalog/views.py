from http import HTTPStatus

from django.http import HttpResponse


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
