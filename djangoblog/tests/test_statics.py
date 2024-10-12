from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

from djangoblog.utils.limit_test import TestCase


class TestStaticFiles(TestCase):
    def test_images(self):
        abs_path = finders.find("/static/styles.css")
        self.assertTrue(staticfiles_storage.exists(abs_path))
