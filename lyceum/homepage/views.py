from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
from homepage.forms import HomepageForm

__all__ = [
    "home",
    "coffee",
]


def home(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main().order_by("name")

    context = {
        "items": items,
    }
    return render(
        request,
        template,
        context,
    )


def coffee(request):
    return HttpResponse(
        "Я чайник",
        status=HTTPStatus.IM_A_TEAPOT,
    )


def echo(request):
    template = "homepage/echo.html"
    form = HomepageForm(request.POST or None)

    if form.is_valid():
        text = form.cleaned_data.get("text")

        return HttpResponse(
            text,
            content_type="text/plain",
        )

    context = {
        "form": form,
    }

    return render(
        request,
        template,
        context,
    )


def echo_submit(request):

    text = request.POST.get("text")

    return HttpResponse(
        text,
        content_type="text/plain",
    )
