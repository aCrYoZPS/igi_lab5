from django.urls import path
from .views import ClientView, UpdateClientView, DeleteClientView

urlpatterns = [
    path("clients/", ClientView.as_view(), name="client_profile"),
    path("clients/<int:pk>/edit/", UpdateClientView.as_view(), name="update_client"),
    path("clients/<int:pk>/delete/", DeleteClientView.as_view(), name="delete_client"),
]
