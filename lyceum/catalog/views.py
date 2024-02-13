from django.http import HttpResponse


def item_list(request):
    return HttpResponse("Список элементов", status=200)


def item_detail(request, item_id):
    return HttpResponse("Подробно элемент", status=200)


def number(request, num):
    return HttpResponse(content=num, status=200)


def converter(request, num):
    return HttpResponse(content=num, status=200)
