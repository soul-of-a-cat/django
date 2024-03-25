import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

import users.forms
import users.models


__all__ = [
    "signup",
    "profile",
    "user_list",
    "user_detail",
    "activate",
]


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)
    template = "users/signup.html"
    context = {
        "form": form,
    }
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=True)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        users.models.Profile(user_id=user.id).save()
        send_mail(
            "Activate account!",
            request.build_absolute_uri(
                reverse("users:activate", kwargs={"pk": user.id}),
            ),
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        username = form.cleaned_data.get("username")
        messages.success(
            request,
            f"Пользователь {username} был успешно создан!",
        )
        return redirect(reverse("homepage:home"))

    return render(request, template, context)


def activate(request, pk: int):
    user = users.models.User.objects.get(id=pk)
    if timezone.now() < user.date_joined + datetime.timedelta(hours=12):
        messages.success(request, "Активация прошла успешно!")
        user.is_active = True
        user.save()
    else:
        messages.error(request, "Ошибка активации!")

    return redirect(reverse("homepage:home"))


def reactivate(request, pk: int):
    user = users.models.User.objects.get(id=pk)
    if timezone.now() < user.date_joined + datetime.timedelta(days=7):
        messages.success(request, "Активация прошла успешно!")
        user.is_active = True
        user.save()
    else:
        messages.error(request, "Ошибка активации!")

    return redirect(reverse("homepage:home"))


def user_list(request):
    users = get_user_model().objects.filter(is_active=True)
    return render(
        request,
        "users/user_list.html",
        {"users": users},
    )


def user_detail(request, num):
    user = get_object_or_404(
        get_user_model().objects.filter(
            is_active=True,
            id=num,
        )
    )
    return render(
        request,
        "users/user_detail.html",
        {"user_item": user},
    )


@login_required
def profile(request):
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
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
            messages.success(request, "Изменения сохранены!")
            return redirect(reverse("homepage:home"))

    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "user_form": user_form,
            "user": request.user,
        },
    )
