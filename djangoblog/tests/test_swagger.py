import json

from django.test.client import Client
from django.test import TestCase

class SwaggerSchemaTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(SwaggerSchemaTest, self).__init__(*args, **kwargs)
        self.client = Client()
        self.response_v1 = self.client.get('http://localhost:8000/api/v1/schema.json')
        self.response_v2 = self.client.get('http://localhost:8000/api/v2/schema.json')
        self.content_v1 = json.loads(self.response_v1.content.decode("utf-8"))
        self.content_v2 = json.loads(self.response_v2.content.decode("utf-8"))

    def test_swagger_schema(self):
        self.assertEquals(self.response_v1.status_code, 200)
        self.assertEquals(self.content_v1["info"]["title"], "Blog API")
        self.assertNotIn("v2", self.content_v1["info"]["version"])


    def test_swagger_schema_version(self):
        pass
        # assert False
