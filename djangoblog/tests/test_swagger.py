import json

from django.test.client import Client
from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment

class SwaggerSchemaTest(TestCase):
    client = Client()

    response_v1 = client.get('http://localhost:8000/api/v1/schema.json')
    response_v2 = client.get('http://localhost:8000/api/v2/schema.json')

    content_v1 = json.loads(response_v1.content.decode("utf-8"))
    content_v2 = json.loads(response_v2.content.decode("utf-8"))

    def test_swagger_schema(self):
        self.assertEquals(self.response_v1.status_code, 200)
        self.assertEquals(self.content_v1["info"]["title"], "Blog API")
        self.assertNotIn("v2", self.content_v1["info"]["version"])

