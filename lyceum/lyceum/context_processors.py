from datetime import datetime

from users.models import User

__all__ = []


def birthday_users(request):
    today = datetime.now().date()
    birthday_users = User.objects.filter(
        profile__birthday__day=today.day,
        profile__birthday__month=today.month,
        is_active=True,
    ).only("profile__birthday", "username", "email")

    return {"birthday_users": birthday_users}
