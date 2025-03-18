from django.test import TestCase
from rest_framework import status

from authentication.models import AuthUser


class TestAuthUser(TestCase):
    def test_sign_up_success(self):
        email = "yysss61888@gmail.com"
        password = "1234"
        username = "yysss61888"
        response = self.client.post("/api/auth/sign-up",
                                    {"email": email, "password": password, "username": username})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        user = AuthUser.objects.get(email=email)
        self.assertEqual(user.email, email)

    def test_sign_up_failure(self):
        email = "yysss61888"
        password = "1234"
        response = self.client.post("/api/auth/sign-up", {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        email = "yysss61888@gmail.com"
        password = "1234"
        AuthUser.objects.create_user(email=email, password=password, username="yysss61888")

        response = self.client.post("/api/auth/login", {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_failure(self):
        email = "yysss61888@gmail.com"
        password = "1234"
        AuthUser.objects.create_user(email=email, password=password, username="yysss61888")

        response = self.client.post("/api/auth/login", {"email": email, "password": "12345"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
