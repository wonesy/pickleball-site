from django.urls import path
from standings import views

urlpatterns = [
    path("", views.standings, name="standings"),
]
