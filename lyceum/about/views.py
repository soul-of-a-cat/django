from django.views import generic

__all__ = [
    "AboutView",
]


class AboutView(generic.TemplateView):
    template_name = "about/about.html"
