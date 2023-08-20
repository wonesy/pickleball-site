# urls.py
from django.urls import path
from matches import views

urlpatterns = [
    path("submit_result/<int:match_id>/", views.submit_result, name="submit_result"),
    path("<str:username>/", views.schedule, name="schedule"),
]
