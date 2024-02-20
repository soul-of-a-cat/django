from http import HTTPStatus

from django.http import HttpResponse


def home(request):
    return HttpResponse("Главная страница", status=HTTPStatus.OK)


def coffee(request):
    return HttpResponse(
        "Я чайник",
        status=HTTPStatus.IM_A_TEAPOT,
    )
