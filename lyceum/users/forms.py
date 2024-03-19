from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

import users.models

__all__ = [
    "ProfileForm",
    "SignUpForm",
    "UserForm",
]


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
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
            model.coffee_count.field.name: forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
            model.birthday.field.name: forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


class UserForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        model = User
        fields = [
            User.email.field.name,
            User.first_name.field.name,
        ]
