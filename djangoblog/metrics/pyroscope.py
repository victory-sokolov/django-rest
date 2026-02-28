import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

PYROSCOPE_DEFAULT_SAMPLE_RATE = 100


def init_pyroscope(app_name: str) -> bool:
    """Initialize Pyroscope profiling for the application.

    Args:
        app_name: The application name to use for profiling (e.g., 'django-blog-gunicorn')

    Returns:
        True if pyroscope was initialized successfully, False otherwise.

    Environment Variables:
        PYROSCOPE_ENABLED: Enable/disable profiling (default: false)
        PYROSCOPE_SERVER_URL: Pyroscope server URL (required if enabled)
        PYROSCOPE_SAMPLE_RATE: Sample rate 1-100 (default: 100)
        PYROSCOPE_TAGS: Comma-separated tags (e.g., 'env:prod,region:us')
    """
    enabled = os.environ.get("PYROSCOPE_ENABLED", "false").lower() in (
        "true",
        "1",
        "yes",
    )

    if not enabled:
        logger.debug("Pyroscope profiling is disabled")
        return False

    server_url = os.environ.get("PYROSCOPE_SERVER_URL")
    if not server_url:
        logger.warning(
            "PYROSCOPE_SERVER_URL not set, skipping pyroscope initialization"
        )
        return False

    try:
        import pyroscope
    except ImportError:
        logger.warning("pyroscope-io package not installed, skipping profiling")
        return False

    sample_rate_str = os.environ.get(
        "PYROSCOPE_SAMPLE_RATE", str(PYROSCOPE_DEFAULT_SAMPLE_RATE)
    )
    try:
        sample_rate = int(sample_rate_str)
        if not 1 <= sample_rate <= 100:
            logger.warning(
                f"PYROSCOPE_SAMPLE_RATE must be between 1 and 100, got {sample_rate}, using default"
            )
            sample_rate = PYROSCOPE_DEFAULT_SAMPLE_RATE
    except ValueError:
        logger.warning(
            f"Invalid PYROSCOPE_SAMPLE_RATE value: {sample_rate_str}, using default"
        )
        sample_rate = PYROSCOPE_DEFAULT_SAMPLE_RATE

    tags: dict[str, Any] = {}
    tags_env = os.environ.get("PYROSCOPE_TAGS")
    if tags_env:
        for tag_pair in tags_env.split(","):
            if ":" in tag_pair:
                key, value = tag_pair.split(":", 1)
                tags[key.strip()] = value.strip()

    try:
        pyroscope.configure(
            application_name=app_name,
            server_address=server_url,
            sample_rate=sample_rate,
            tags=tags,
        )
        logger.info(f"Pyroscope initialized for '{app_name}' with server {server_url}")
        return True
    except Exception:
        logger.exception("Failed to initialize pyroscope")
        return False
