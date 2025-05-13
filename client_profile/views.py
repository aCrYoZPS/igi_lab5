from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, DeleteView
from cleaning_service.models import Client
from django.views.generic import DetailView


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "service/client_profile.html"
    context_object_name = "client"

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = [
        "name", "contact_person", "contact_number",
        "email", "client_type", "address", "timezone"
    ]
    template_name = "service/client_edit.html"
    success_url = reverse_lazy("client_profile")

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        return form


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)

    def form_valid(self, form):
        user = self.object.user
        response = super().form_valid(form)
        user.delete()
        logout(self.request)
        return response
