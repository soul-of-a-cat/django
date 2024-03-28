from django.views import generic

__all__ = []


class AboutView(generic.TemplateView):
    template_name = "about/about.html"
