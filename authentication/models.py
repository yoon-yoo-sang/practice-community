from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class AuthUser(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "user"
