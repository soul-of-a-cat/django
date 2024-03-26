from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

import catalog.models
from homepage.forms import HomepageForm

__all__ = [
    "HomeView",
    "CoffeeView",
    "EchoView",
    "EchoSubmitView",
]


class HomeView(generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.on_main().order_by("name")


class CoffeeView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()

        return HttpResponse(
            "Я чайник",
            status=HTTPStatus.IM_A_TEAPOT,
        )


class EchoView(generic.View):
    def get(self, request):
        template = "homepage/echo.html"
        homepage_form = HomepageForm(request.GET or None)
        context = {"form": homepage_form, "echo": True}
        return render(
            request,
            template,
            context,
        )


class EchoSubmitView(generic.View):
    def post(self, request):
        text = request.POST.get("text")
        return HttpResponse(text)
