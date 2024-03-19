from http import HTTPStatus

from django.contrib import messages
import django.contrib.auth.decorators
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
from homepage.forms import HomepageForm
import users.forms

__all__ = [
    "home",
    "coffee",
    "echo",
    "echo_submit",
    "profile",
]


def home(request):
    if not request.user.is_active:
        messages.error(request, "Вы не зарегистрированы!")

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


@django.contrib.auth.decorators.login_required
def profile(request):
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )
    user_form = users.forms.UserForm(
        request.POST or None,
        instance=request.user,
    )
    if request.method == "POST":
        if all((profile_form.is_valid(), user_form.is_valid())):
            profile_form.save()
            user_form.save()

    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "user_form": user_form,
            "user": request.user,
        },
    )
