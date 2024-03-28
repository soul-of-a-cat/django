import re

from django.conf import settings

__all__ = []


def reverse_words(text):
    pattern = re.compile(
        r"\b[а-яё]+\b",
        re.IGNORECASE,
    )

    for m in re.finditer(string=text, pattern=pattern):
        s = m.start()
        e = m.end()
        text = text[:s] + text[s:e][::-1] + text[e:]

    return text


class ReverseResponseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        cls.count = (cls.count + 1) % 10
        if cls.count == 0:
            return True

        return False

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode("utf-8")

        rev_content = reverse_words(content).encode("utf-8")

        response.content = rev_content
        return response
