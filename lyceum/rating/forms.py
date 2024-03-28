import django.forms

import rating.models

__all__ = []


class RatingForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-select"

        self.fields[rating.models.Rating.rating.field.name].widget.attrs[
            "onchange"
        ] = "this.form.submit()"
        self.fields[rating.models.Rating.user.field.name].disabled = True
        self.fields[rating.models.Rating.item.field.name].disabled = True

    class Meta:
        model = rating.models.Rating
        fields = (
            model.user.field.name,
            model.item.field.name,
            model.rating.field.name,
        )
        widgets = {
            model.user.field.name: django.forms.HiddenInput(),
            model.item.field.name: django.forms.HiddenInput(),
        }
