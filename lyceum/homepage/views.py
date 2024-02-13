from django.http import HttpResponse
from rest_framework import status

# from rest_framework.decorators import api_view
# from rest_framework.response import Response


def home(request):
    return HttpResponse("Главная", status=200)


def coffee(request):
    content = "Я чайник"
    return HttpResponse(
        content=content, status=status.HTTP_418_IM_A_TEAPOT, charset="utf-8"
    )
