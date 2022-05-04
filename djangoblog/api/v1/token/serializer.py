from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from django.conf import settings


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
