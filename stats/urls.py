from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.StatsView.as_view(), name="stats"),
]
