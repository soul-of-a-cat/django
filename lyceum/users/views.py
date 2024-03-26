import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

import users.forms
import users.models

__all__ = [
    "Signup",
    "Activate",
    "Reactivate",
    "UserListView",
    "UserDetailView",
    "ProfileView",
]


class Signup(generic.CreateView):
    template_name = "users/signup.html"
    form_class = users.forms.SignUpForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save(commit=True)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        users.models.Profile(user_id=user.id).save()
        send_mail(
            "Activate account!",
            self.request.build_absolute_uri(
                reverse("users:activate", kwargs={"pk": user.id}),
            ),
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        username = form.cleaned_data.get("username")
        messages.success(
            self.request,
            f"Пользователь {username} был успешно создан!",
        )
        return redirect(reverse("homepage:home"))


class Activate(generic.DetailView):
    queryset = users.models.User.objects.all()

    def get(self, *args, pk):
        user = self.get_object(self.queryset)
        if timezone.now() < user.date_joined + datetime.timedelta(hours=12):
            messages.success(self.request, "Активация прошла успешно!")
            user.is_active = True
            user.save()
        else:
            messages.error(self.request, "Ошибка активации!")

        return redirect(reverse("homepage:home"))


class Reactivate(generic.DetailView):
    queryset = users.models.User.objects.all()

    def get(self, *args, pk):
        user = self.get_object(self.queryset)
        if timezone.now() < user.date_joined + datetime.timedelta(days=7):
            messages.success(self.request, "Активация прошла успешно!")
            user.is_active = True
            user.save()
        else:
            messages.error(self.request, "Ошибка активации!")

        return redirect(reverse("homepage:home"))


class UserListView(generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = "users"
    queryset = users.models.User.objects.active()


class UserDetailView(generic.DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user_item"
    queryset = users.models.User.objects.active()


class ProfileView(LoginRequiredMixin, generic.CreateView):
    template_name = "users/profile.html"
    form_class = users.forms.UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update(
            instance={
                "user": self.request.user,
                "profile": self.request.user.profile,
            },
        )
        return kwargs

    def form_valid(self, form):
        profile_form = form["profile"]
        user_form = form["user"]
        profile_form.save()
        user_form.save()
        messages.success(self.request, "Изменения сохранены!")
        return redirect(reverse("homepage:home"))
