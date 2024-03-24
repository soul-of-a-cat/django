from django.contrib.auth.forms import UserCreationForm
import django.forms

import users.models


__all__ = [
    "ProfileForm",
    "SignUpForm",
    "CustomUserChangeForm",
]


class ProfileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]
        widgets = {
            model.coffee_count.field.name: django.forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
            model.birthday.field.name: django.forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


class CustomUserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
