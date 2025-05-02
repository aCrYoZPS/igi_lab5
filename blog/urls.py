from django.urls import path
from . import views

urlpatterns = [
    path("articles/<int:article_id>/", views.article, name="article"),
    path("articles/", views.ArticlesView.as_view(), name="articles")
]
