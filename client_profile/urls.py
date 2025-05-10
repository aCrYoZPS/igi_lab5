from django.urls import path
from .views import ClientDetailView, ClientUpdateView, ClientDeleteView

urlpatterns = [
    path("client/", ClientDetailView.as_view(), name="client_profile"),
    path("client/edit/", ClientUpdateView.as_view(), name="client_edit"),
    path("client/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
