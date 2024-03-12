from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


__all__ = [
    "feedback",
]


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data.get("name")
        text = form.cleaned_data.get("text")
        user_mail = form.cleaned_data.get("mail")
        django_mail = settings.EMAIL_HOST_USER
        message = f"Name: {name}\nMessage: {text}"
        send_mail(
            "Subject here",
            message,
            django_mail,
            [user_mail],
        )

        messages.success(request, "Форма успешно отправлена!")

        return redirect("feedback:feedback")

    context = {
        "form": form,
    }

    return render(
        request,
        template,
        context,
    )
