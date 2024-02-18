import itertools

import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class StaticUrlTests(APITestCase):
    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.parameterized.expand(
        [
            ("1", status.HTTP_200_OK),
            ("100", status.HTTP_200_OK),
            ("0", status.HTTP_200_OK),
            ("-0", status.HTTP_404_NOT_FOUND),
            ("-100", status.HTTP_404_NOT_FOUND),
            ("0.5", status.HTTP_404_NOT_FOUND),
            ("abc", status.HTTP_404_NOT_FOUND),
            ("0abc", status.HTTP_404_NOT_FOUND),
            ("abc0", status.HTTP_404_NOT_FOUND),
            ("$%^", status.HTTP_404_NOT_FOUND),
            ("1e5", status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = self.client.get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.parameterized.expand(
        map(
            lambda x: (x[0], x[1][0], x[1][1]),
            itertools.product(
                ["converter", "re"],
                [
                    ("1", status.HTTP_200_OK),
                    ("100", status.HTTP_200_OK),
                    ("0", status.HTTP_200_OK),
                    ("-0", status.HTTP_404_NOT_FOUND),
                    ("-100", status.HTTP_404_NOT_FOUND),
                    ("0.5", status.HTTP_404_NOT_FOUND),
                    ("abc", status.HTTP_404_NOT_FOUND),
                    ("0abc", status.HTTP_404_NOT_FOUND),
                    ("abc0", status.HTTP_404_NOT_FOUND),
                    ("$%^", status.HTTP_404_NOT_FOUND),
                    ("1e5", status.HTTP_404_NOT_FOUND),
                ],
            ),
        )
    )
    def test_catalog_item_pint_endpoint(
        self,
        prefix,
        url,
        expected_status,
    ):
        full_url = f"/catalog/{prefix}/{url}/"
        response = self.client.get(full_url)
        self.assertEqual(
            response.status_code,
            expected_status,
            f"failed check status request to {full_url}",
        )
