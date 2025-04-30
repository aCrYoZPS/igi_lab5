from django.urls import path, include
from . import views

urlpatterns = [
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/signup/", views.signup, name='signup'),
]
