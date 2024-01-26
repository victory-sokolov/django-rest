import json

from django.test import TestCase
from django.test.client import Client


class TestSwaggerSchema(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()
        self.response_v1 = self.client.get("/api/v1/schema.json")
        self.content_v1 = json.loads(self.response_v1.content.decode("utf-8"))

    def test_swagger_schema(self):
        self.assertEqual(self.response_v1.status_code, 200)
        self.assertEqual(self.content_v1["info"]["title"], "Blog API")
        self.assertNotIn("v2", self.content_v1["info"]["version"])
