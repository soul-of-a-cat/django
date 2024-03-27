from django.apps import AppConfig

__all__ = [
    "StatisticsRatingConfig",
]


class StatisticsRatingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statistics_rating"
    verbose_name = "Статистика"
