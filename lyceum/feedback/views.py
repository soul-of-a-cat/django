from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import generic

from feedback.forms import FeedbackAuthorForm, FeedbackFileForm, FeedbackForm
from feedback.models import FeedbackFile

__all__ = [
    "FeedbackView",
]


class FeedbackView(generic.View):
    template_name = "feedback/feedback.html"

    def get(self, request):
        feedback_form = FeedbackForm()
        author_form = FeedbackAuthorForm()
        files_form = FeedbackFileForm()
        context = {
            "form": feedback_form,
            "author_form": author_form,
            "files_form": files_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        feedback_form = FeedbackForm(request.POST)
        author_form = FeedbackAuthorForm(request.POST)
        files_form = FeedbackFileForm(request.POST, request.FILES)

        if (
            feedback_form.is_valid()
            and author_form.is_valid()
            and files_form.is_valid()
        ):
            mail = author_form.cleaned_data["mail"]
            name = author_form.cleaned_data["name"]
            text = feedback_form.cleaned_data["text"]

            feedback = feedback_form.save()
            author = author_form.save(commit=False)
            author.feedback = feedback
            author.save()

            files = files_form.cleaned_data["files"]
            for file in files:
                FeedbackFile.objects.create(
                    file=file,
                    feedback=feedback,
                )

            email_dear = "feedback__email__dear"
            email_text = "feedback__email__text"
            send_mail(
                "feedback__email__title",
                (f"{email_dear} {name},\n\n" if name else "")
                + f"{email_text}\n{text}",
                None,
                [mail],
                fail_silently=False,
            )
            messages.success(request, "feedback__email__success")
            return redirect("feedback:feedback")

        return None
