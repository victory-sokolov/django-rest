import json

from django.test import TestCase
from django.test.client import Client


class TestSwaggerSchema(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.response_v1 = cls.client.get("/api/v1/schema.json")
        cls.content_v1 = json.loads(cls.response_v1.content.decode("utf-8"))

    def test_swagger_schema(self):
        self.assertEqual(self.response_v1.status_code, 200)
        self.assertEqual(self.content_v1["info"]["title"], "Blog API")
        self.assertNotIn("v2", self.content_v1["info"]["version"])
