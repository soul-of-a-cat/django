from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
from homepage.forms import HomepageForm

__all__ = [
    "home",
    "coffee",
    "echo",
    "echo_submit",
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
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.coffee_count += 1
        profile.save()

    return HttpResponse(
        "Я чайник",
        status=HTTPStatus.IM_A_TEAPOT,
    )


def echo(request: HttpResponse) -> HttpResponse:
    if request.method == "GET":
        template = "homepage/echo.html"
        homepage_form = HomepageForm(request.GET or None)
        context = {"form": homepage_form, "echo": True}

        return render(
            request,
            template,
            context,
        )

    return HttpResponseNotAllowed(["GET"])


def echo_submit(request):
    if request.method == "POST":
        text = request.POST.get("text")

        return HttpResponse(text)

    return HttpResponseNotAllowed(["POST"])
