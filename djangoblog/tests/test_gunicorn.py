import sys
from unittest import mock

from django.test import SimpleTestCase

from gunicorn.app.wsgiapp import run


class GunicornConfigTests(SimpleTestCase):
    def test_config(self):
        argv = [
            "gunicorn",
            "--check-config",
            "--config",
            "gunicorn_config.py",
            "djangoblog.wsgi:application",
        ]
        mock_argv = mock.patch.object(sys, "argv", argv)

        with self.assertRaises(SystemExit) as cm, mock_argv:
            run()

        exit_code = cm.exception.args[0]
        self.assertEqual(exit_code, 0)
