from datetime import datetime

from users.models import User

__all__ = [
    "birthday_users",
]


def birthday_users(request):
    today = datetime.now().date()
    birthday_users = User.objects.filter(
        profile__birthday__day=today.day, profile__birthday__month=today.month
    )

    return {
        "birthday_users": ", ".join([user.username for user in birthday_users])
    }
