from betterforms.multiform import MultiModelForm
import django.forms

import feedback.models

__all__ = [
    "FeedbackForm",
    "FeedbackAuthorForm",
    "FeedbackFileForm",
    "FeedbackMultiForm",
]


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.Feedback
        exclude = [
            feedback.models.Feedback.created_on.field.name,
            feedback.models.Feedback.status.field.name,
        ]


class FeedbackAuthorForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.FeedbackAuthor
        exclude = [
            feedback.models.FeedbackAuthor.feedback.field.name,
        ]
        error_messages = {
            feedback.models.FeedbackAuthor.mail.field.name: {
                "required": "Введите правильный адрес электронной почты."
            }
        }


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)


class FeedbackFileForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    files = MultipleFileField(required=False, label="Файлы")


class FeedbackMultiForm(MultiModelForm):
    form_classes = {
        "content": FeedbackForm,
        "author": FeedbackAuthorForm,
        "files": FeedbackFileForm,
    }
