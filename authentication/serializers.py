from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import AuthUser


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AuthUser
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        if not self.check_valid_email(attrs["email"]):
            raise serializers.ValidationError("Invalid email")
        if not attrs["email"] or not attrs["password"]:
            raise serializers.ValidationError("Email and password are required.")
        return attrs

    def create(self, validated_data):
        user = AuthUser.objects.create_user(**validated_data)
        return user

    @staticmethod
    def check_valid_email(email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return email
