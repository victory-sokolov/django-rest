from jwt import InvalidTokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.conf import settings

from django.utils.translation import gettext_lazy as _


class Cutsom(InvalidTokenError):
    error_type = "My Custom type"


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data["access_token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        data["expiry_in"] = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        return data


class RefreshToken(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["access_token"] = data.pop("access")
        data["expiry_in"] = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        return data
