from typing import Callable

from django.http import HttpRequest, HttpResponse

from users.models import User

__all__ = [
    "UserMiddleware",
]


class UserMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user = User.objects.get(id=request.user.id)

        return self.get_response(request)
