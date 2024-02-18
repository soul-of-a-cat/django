from django.http import HttpResponse
from rest_framework import status


def home(request):
    return HttpResponse("Главная страница", status=status.HTTP_200_OK)


def coffee(request):
    return HttpResponse(
        "Я чайник",
        status=status.HTTP_418_IM_A_TEAPOT,
    )
