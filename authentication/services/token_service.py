from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser


class TokenService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TokenService, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def create_token(user: AuthUser) -> dict:
        token = RefreshToken.for_user(user)
        return {
            "access_token": str(token.access_token),
            "refresh_token": str(token),
        }
