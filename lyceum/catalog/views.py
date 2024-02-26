from http import HTTPStatus

from django.http import HttpResponse

from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(
        request,
        template,
        context,
    )


def item_detail(request, num):
    return HttpResponse(
        "Подробно элемент",
        status=HTTPStatus.OK,
    )
