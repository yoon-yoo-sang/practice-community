from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import AuthUser
from authentication.serializers import AuthUserSerializer
from authentication.services.token_service import TokenService


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if AuthUser.objects.filter(email=email).exists():
            return Response(
                {"detail": "User already exists."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = TokenService.create_token(user)
        return Response(token, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = AuthUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
            )

        token = TokenService.create_token(user)
        return Response(token, status=status.HTTP_200_OK)
