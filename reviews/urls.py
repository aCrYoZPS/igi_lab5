from django.urls import path, re_path
from . import views

urlpatterns = [
    path("reviews/", views.ReviewView.as_view(), name="reviews"),
    path("review/add/", views.AddReviewView.as_view(), name="add_review"),
    re_path(r"^review/edit/(?P<pk>\d+)/$", views.UpdateReviewView.as_view(), name="edit_review"),
]
