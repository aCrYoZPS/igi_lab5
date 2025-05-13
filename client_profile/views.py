from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from cleaning_service.models import Client
from .forms import ClientForm


User = get_user_model()


class ClientView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "service/client_profile.html"
    context_object_name = "client"

    def get_object(self):
        return self.request.user.client_profile


class UpdateClientView(LoginRequiredMixin, UpdateView):
    form_class = ClientForm
    template_name = "service/client_edit.html"
    success_url = reverse_lazy('client_profile')

    def get_object(self):
        return self.request.user.client_profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.client_profile
        return kwargs


class DeleteClientView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "service/confirm_client_deletion.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response
