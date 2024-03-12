from django import forms

__all__ = [
    "FeedbackForm",
]


class FeedbackForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        help_text="Напишите текст сообщения",
        widget=forms.Textarea,
    )
    mail = forms.EmailField(
        label="Почта",
        max_length=100,
        help_text="Почтовый адрес",
    )
