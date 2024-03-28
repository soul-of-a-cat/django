from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

import users.models

__all__ = []

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = users.models.Profile
    fields = [
        users.models.Profile.birthday.field.name,
        users.models.Profile.image.field.name,
        users.models.Profile.coffee_count.field.name,
    ]
    readonly_fields = (users.models.Profile.coffee_count.field.name,)
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [
        ProfileInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
