import re

from django.conf import settings


class ReverseResponseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            if self.__class__.count == 9:
                content = response.content.decode("utf-8")
                russian_words = re.findall("[а-яА-ЯёЁ]+", content)
                for word in russian_words:
                    content = content.replace(word, word[::-1])
                response.content = content.encode("utf-8")
                self.__class__.count = 0
                return response
            self.__class__.count += 1
        return response
