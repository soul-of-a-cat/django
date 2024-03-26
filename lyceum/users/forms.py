from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import UserCreationForm
import django.forms

import users.models


__all__ = [
    "ProfileForm",
    "SignUpForm",
    "UserForm",
    "UserProfileForm",
]


class ProfileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        coffee = users.models.Profile.coffee_count.field.name
        self.fields[coffee].disabled = True

    class Meta:
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]
        widgets = {
            model.birthday.field.name: django.forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


class UserForm(django.contrib.auth.forms.UserChangeForm):
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


class UserProfileForm(MultiModelForm):
    form_classes = {
        "user": UserForm,
        "profile": ProfileForm,
    }
