from django.http import HttpResponse
from rest_framework import status


def home(request):
    return HttpResponse("Главная", status=200)


def coffee(request):
    content = "Я чайник"
    return HttpResponse(
        content=content, status=status.HTTP_418_IM_A_TEAPOT, charset="utf-8"
    )
