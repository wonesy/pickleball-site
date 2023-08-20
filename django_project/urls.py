from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("schedule/", include("matches.urls")),
    path("standings/", include("standings.urls")),
    path("", include("pages.urls")),
]
