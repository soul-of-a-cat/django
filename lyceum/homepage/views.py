from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    return HttpResponse("Главная", status=200)


@api_view(["GET"])
def coffee(request):
    return Response("Я чайник", status=status.HTTP_418_IM_A_TEAPOT)
