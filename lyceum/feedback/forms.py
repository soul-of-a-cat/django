from django import forms

__all__ = [
    "FeedbackForm",
]


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имя пользователя",
        help_text="Напишите своё имя",
        error_messages={
            'required': 'Please enter your name'
        },
    )
    text = forms.CharField(
        label="Текст",
        help_text="Напишите текст сообщения",
        widget=forms.Textarea(attrs={"class": "my-field"}),
        error_messages={
            'required': 'Please enter text'
        },
    )
    mail = forms.EmailField(
        label="Почта",
        max_length=100,
        help_text="Почтовый адрес",
        error_messages={
            'required': 'Please enter your email'
        },
    )
