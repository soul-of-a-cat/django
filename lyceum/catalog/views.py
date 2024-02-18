from django.http import HttpResponse
from rest_framework import status


def item_list(request):
    return HttpResponse("Список элементов", status=status.HTTP_200_OK)


def item_detail(request, num):
    return HttpResponse("Подробно элемент", status=status.HTTP_200_OK)
