# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def item_list(request):
    return HttpResponse("Список элементов", status=200)


def item_detail(request, item_id):
    return HttpResponse("Подробно элемент", status=200)
