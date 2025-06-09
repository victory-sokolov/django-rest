import logging
from prometheus_client import start_http_server, CollectorRegistry

logger = logging.getLogger(__name__)


def start_prometheus_server(collector_registry: CollectorRegistry) -> None:
    """Start the Prometheus metrics server."""
    port = 8004
    start_http_server(port=port, registry=collector_registry)
    logger.info(f"Running Prometheus server on port {port}")
