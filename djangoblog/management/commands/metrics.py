import logging

from django.core.management.base import BaseCommand
from prometheus_client import (
    CollectorRegistry,
)

from djangoblog.metrics.monitor import start_prometheus_server

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for metrics server."""

    help = "Start metrics server"

    def handle(self, *args: list, **options: list) -> None:
        registry = CollectorRegistry()
        start_prometheus_server(registry)
