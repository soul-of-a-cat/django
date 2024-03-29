from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

import users.models

__all__ = []


class UserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None
        else:
            if not hasattr(user, f"{users.models.User.profile.related.name}"):
                users.models.Profile.objects.create(user=user)

            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            user.profile.attempts_count += 1
            if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
                user.is_active = False
                user.profile.block_date = timezone.now()
                user.save()
                send_mail(
                    "Activate account!",
                    request.build_absolute_uri(
                        reverse("users:reactivate", kwargs={"pk": user.id}),
                    ),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

            user.profile.save()

        return None
