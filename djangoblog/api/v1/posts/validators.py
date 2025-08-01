import logging
from typing import OrderedDict

from djangoblog.api.error import PostException

logger = logging.getLogger(__name__)


class TitleValidator:
    MIN_TITLE_LENGTH = 10

    def __call__(self, title: str) -> None:
        logger.info(f"Validating title: {title}")
        if len(title) < self.MIN_TITLE_LENGTH:
            raise PostException.validation_error(
                f"Min title length is {self.MIN_TITLE_LENGTH}",
                "Title",
            )


class SlugValidator:
    MIN_SLUG_LENGTH = 3

    def __call__(self, slug: str) -> None:
        logger.info(f"Validating Slug: {slug}")
        if len(slug) < self.MIN_SLUG_LENGTH:
            raise PostException.validation_error(
                f"Slug must be at least {self.MIN_SLUG_LENGTH} characters long",
                "slug",
            )


class TagValidator:
    def __call__(self, tags: OrderedDict[str, str]) -> None:
        logger.info(f"Validating Tags: {tags}")
        tag = list(tags.values())[0]
        errors = []

        if " " in tag:
            errors.append(f"'{tag}' should not contain spaces")
        if len(errors) > 0:
            raise PostException.validation_error(
                errors,
                "Tag",
            )
