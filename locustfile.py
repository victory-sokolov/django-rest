import logging
import os
import random
import string

from locust import HttpUser, task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ListPostUser(HttpUser):
    # local base_url
    # base_url = "http://localhost:8000/api/v1"

    # Docker base_url
    base_url = "http://0.0.0.0:80/api/v1"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOKEN')}",
        # "Connection": "keep-alive",
        "User-Agent": "Locust",
    }

    @task
    def get_posts(self):
        response = self.client.get(
            headers=self.headers,
            url=f"{self.base_url}/post/",
            verify=False,
        )
        logger.info(response.status_code)

    def generate_random_slug(self, length: int):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = "".join(random.choice(letters_and_digits) for i in range(length))
        return result_str

    @task
    def create_post(self):
        response = self.client.post(
            verify=False,
            headers=self.headers,
            url=f"{self.base_url}/post/",
            json={
                "title": "Test post",
                "content": "Random content data",
                "slug": self.generate_random_slug(10),
            },
        )
        logger.info(response.status_code)
