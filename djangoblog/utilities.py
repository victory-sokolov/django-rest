import inspect
import logging

from typing import Any, Callable

logger = logging.getLogger(__name__)


def slugify(content: str) -> str:
    return content.lower().replace(" ", "-").replace(",", "")


def enable_args_debugger(func: Callable) -> Callable:
    """Decorator to print function call details and parameters names and values."""

    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(
            map("{0[0]} = {0[1]!r}".format, func_args.items()),
        )
        logger.debug(
            f"{func.__module__}.{func.__qualname__} ( {func_args_str})",
        )
        return func(*args, **kwargs)

    return wrapper
