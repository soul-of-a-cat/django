import re

from django.conf import settings

WORDS_REGEX = re.compile(r"\w+|\W+")
NOT_RUSSIAN_REGEX = re.compile(r"^[^а-яА-Я\s]+$")

__all__ = [
    "ReverseResponseMiddleware",
    "reverse_words",
]


def reverse_words(content):
    words = WORDS_REGEX.findall(content)

    transformed = [
        word if NOT_RUSSIAN_REGEX.search(word) else word[::-1]
        for word in words
    ]

    rev_content = "".join(transformed).encode()
    return rev_content


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
        content = response.content.decode()

        rev_content = reverse_words(content)

        response.content = rev_content
        return response
