from django.http import HttpResponse
from rest_framework import status


def description(request):
    return HttpResponse("О проекте", status=status.HTTP_200_OK)
