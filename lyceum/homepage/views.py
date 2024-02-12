from django.http import HttpResponse
from rest_framework import status

# from rest_framework.decorators import api_view
# from rest_framework.response import Response


def home(request):
    return HttpResponse("Главная", status=200)


def coffee(request):
    content = {"header": "I am a teapot"}
    return HttpResponse(headers=content, status=status.HTTP_418_IM_A_TEAPOT)
