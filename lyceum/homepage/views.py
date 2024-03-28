from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

import catalog.models
from homepage.forms import HomepageForm

__all__ = []


class HomeView(generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.on_main().order_by(
        catalog.models.Item.name.field.name,
    )


class CoffeeView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()

        return HttpResponse(
            _("Я чайник"),
            status=HTTPStatus.IM_A_TEAPOT,
        )


class CoffeeProfileView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()

        return redirect(reverse("users:profile"))


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
