from django.http import HttpResponse
from rest_framework import status


def item_list(request):
    return HttpResponse("Список элементов", status=status.HTTP_200_OK)


def item_detail(request, item_id):
    return HttpResponse("Подробно элемент", status=status.HTTP_200_OK)


def number(request, num):
    if int(num) <= 0 or num[0] == "0":
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(content=num, status=status.HTTP_200_OK)


def converter(request, num):
    if int(num) <= 0 or num[0] == "0":
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(content=num, status=status.HTTP_200_OK)
