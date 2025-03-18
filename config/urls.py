from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # authentication
    path("auth/", include(("authentication.urls", "auth"), namespace="auth")),
    # community
    path("community/", include(("community.urls", "community"), namespace="community")),
]
