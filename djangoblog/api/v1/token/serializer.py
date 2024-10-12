from django.conf import settings
from jwt import InvalidTokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class Cutsom(InvalidTokenError):
    error_type = "My Custom type"


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        data["access_token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        data["expiry_in"] = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        return data


class RefreshToken(TokenRefreshSerializer):
    def validate(self, attrs: dict) -> dict[str, str]:
        data = super().validate(attrs)
        data["access_token"] = data.pop("access")
        data["expiry_in"] = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        return data
