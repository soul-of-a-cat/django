from django import forms

__all__ = [
    "HomepageForm",
]


class HomepageForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        help_text="Напишите текст сообщения",
        widget=forms.Textarea,
    )
