from rest_framework.serializers import ValidationError

class TitleValidator:
    
    MIN_TITLE_LENGTH = 20
    
    def __call__(self, title: str):
        if len(title) < self.MIN_TITLE_LENGTH:
            raise ValidationError(f"Min title length is {self.MIN_TITLE_LENGTH}")
        return title


class SlugsValidator:

    requires_context = True
    
    def __call__(self, slug: str, serializer_field):
        if len(slug) < 10:
            raise ValidationError("Slug must be at least 10 characters long")
        return slug
