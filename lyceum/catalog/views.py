from django.http import HttpResponse
from rest_framework import status


def item_list(request):
    return HttpResponse("Список элементов", status=200)


def item_detail(request, item_id):
    return HttpResponse("Подробно элемент", status=200)


def number(request, num):
    if int(num) <= 0:
        return HttpResponse(status=404)
    return HttpResponse(content=num, status=status.HTTP_200_OK)


def converter(request, num):
    if int(num) <= 0:
        return HttpResponse(status=404)
    return HttpResponse(content=num, status=200)
