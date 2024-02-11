# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def description(request):
    return HttpResponse("О проекте", status=200)
