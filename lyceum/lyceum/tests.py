from rest_framework.test import APITestCase


class MiddleWareTests(APITestCase):
    def test_reverse_middleware(self):
        for i in range(10):
            response = self.client.get("/homepage/coffee/")
            if i == 9:
                self.assertEqual(response.content.decode("utf-8"), "Я кинйач")
