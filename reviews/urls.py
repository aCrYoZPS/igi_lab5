from django.urls import path
from . import views

urlpatterns = [
    path("reviews/", views.ReviewView.as_view(), name="reviews"),
    path("add_review/", views.ReviewView.as_view(), name="add_review")
]
