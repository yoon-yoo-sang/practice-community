from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),

    # authentication
    path("auth/", include(("authentication.urls", "auth"), namespace="auth")),
]
