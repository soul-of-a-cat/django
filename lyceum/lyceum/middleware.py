import re

from django.conf import settings

class ReverseResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            if self.count == 9:
                content = response.content.decode("utf-8")
                russian_words = re.findall("[а-яА-ЯёЁ]+", content)
                for word in russian_words:
                    content = content.replace(word, word[::-1])
                response.content = content.encode("utf-8")
                self.count = 0
                return response
            self.count += 1
        return response
