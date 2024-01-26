from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from djangoblog.api.v1.token.serializer import RefreshToken, TokenSerializer


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshToken
