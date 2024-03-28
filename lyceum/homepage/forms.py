from django import forms
from django.utils.translation import gettext_lazy as _

__all__ = []


class HomepageForm(forms.Form):
    text = forms.CharField(
        label=_("Текст"),
        help_text=_("Напишите текст сообщения"),
        widget=forms.Textarea,
    )
