from django.contrib import admin

import rating.models

__all__ = []


@admin.register(rating.models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        rating.models.Rating.user.field.name,
        rating.models.Rating.item.field.name,
        rating.models.Rating.rating.field.name,
        rating.models.Rating.updated.field.name,
    )
