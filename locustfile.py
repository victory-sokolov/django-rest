import os
import random
import string

from locust import HttpUser, task


class ListPostUser(HttpUser):
    base_url = "https://localhost:8000/api/v1"
    headers = {"Authorization": f"Bearer f{os.getenv('TOKEN')}"}

    @task
    def post_detail(self):
        response = self.client.get(
            headers=self.headers, url=f"{self.base_url}/post/", verify=False
        )
        print(response.json())

    def generate_random_slug(self, length: int):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = "".join(random.choice(letters_and_digits) for i in range(length))
        return result_str

    # @task
    # def create_post(self):
    #     response = self.client.post(
    #         verify=False,
    #         headers=self.headers,
    #         url=f"{self.base_url}/post/",
    #         json={
    #             "title": "Test post",
    #             "content": "Random content data",
    #             "slug": self.generate_random_slug(10),
    #         },
    #     )
    #     print(response.json())
