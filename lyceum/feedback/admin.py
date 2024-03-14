from django.contrib import admin

import feedback.models


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.status.field.name,
    )
    list_display_links = (feedback.models.Feedback.text.field.name,)
    readonly_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.mail.field.name,
    )
    fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.created_on.field.name,
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        feedback.models.StatusLog.objects.create(
            user=request.user,
            from_status=feedback.models.Feedback.objects.get(id=obj.id).status,
            to_status=obj.status,
        )
        super().save_model(request, obj, form, change)
