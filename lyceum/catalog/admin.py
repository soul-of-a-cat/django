from django.contrib import admin
import django.db.models
from mdeditor.widgets import MDEditorWidget
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models
import feedback.models

__all__ = [
    "CategoryAdmin",
    "TagAdmin",
    "ItemAdmin",
    "ItemMainImageAdmin",
    "ItemSecondaryImageAdmin",
]


class ItemMainImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.ItemMainImage


class ItemSecondaryImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.ItemSecondaryImage


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {
            "widget": MDEditorWidget,
        },
    }
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    readonly_fields = (
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    )

    inlines = [
        ItemMainImageInline,
        ItemSecondaryImageInline,
    ]


@admin.register(catalog.models.ItemMainImage)
class ItemMainImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.ItemMainImage.image_tmb.field_name,
        catalog.models.ItemMainImage.item.field.name,
    )


@admin.register(catalog.models.ItemSecondaryImage)
class ItemSecondaryImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.ItemSecondaryImage.image_tmb.field_name,
        catalog.models.ItemSecondaryImage.item.field.name,
    )


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)
    list_display_links = (catalog.models.Tag.name.field.name,)
    tag_name = catalog.models.Tag.name.field.name
    prepopulated_fields = {
        catalog.models.Tag.slug.field.name: (tag_name,),
    }


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.weight.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)
    list_display_links = (catalog.models.Category.name.field.name,)
    category_name = catalog.models.Category.name.field.name
    prepopulated_fields = {
        catalog.models.Category.slug.field.name: (category_name,),
    }


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
    fieldsets = (
        (None,
         {
             'fields': (
                 feedback.models.Feedback.name.field.name,
                 feedback.models.Feedback.text.field.name,
                 feedback.models.Feedback.mail.field.name,
                 feedback.models.Feedback.status.field.name,
                 feedback.models.Feedback.created_on.field.name,
             )
         }
         ),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        feedback.models.StatusLog.objects.create(
            user=request.user,
            from_status=feedback.models.Feedback.objects.get(id=obj.id).status,
            to_status=obj.status,
        )
        super().save_model(request, obj, form, change)
