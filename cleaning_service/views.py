from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from blog.models import Article
from .models import FAQ, Vacancy, About, PrivacyPolicy, PromoCode, ServiceType, Service, Order, OrderItem, Client
from .filters import ServiceFilter
from globals.logging import LoggingMixin
from globals.utils import get_tz
from django_filters.views import FilterView
from .forms import OrderItemFormSet, OrderForm

import json
import requests
from http import HTTPStatus


def index(request):
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code != HTTPStatus.OK:
            ip = "Unable to connect to ip server :("
        else:
            ip = json.loads(response.content)["ip"] + ":>"

    except Exception:
        ip = "Unable to connect to server :("

    return render(request, "service/index.html", {"article": Article.objects.last(), "ip": ip, "tz_info": get_tz(request.user)})


def privacy_policy(request):
    return render(request, "service/privacy_policy.html", {"policy": PrivacyPolicy.objects.last(), "tz_info": get_tz(request.user)})


def faq(request):
    return render(request, "service/faq.html", {"faqs": FAQ.objects.all(), "tz_info": get_tz(request.user)})


def vacancies(request):
    return render(request, "service/vacancies.html", {"vacancies": Vacancy.objects.all(), "tz_info": get_tz(request.user)})


def about(request):
    return render(request, "service/about.html", {"about": About.objects.last(), "tz_info": get_tz(request.user)})


class CatFactView(LoggingMixin, TemplateView):
    template_name = "service/cat_fact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tz_info"] = get_tz(self.request.user)

        try:
            response = requests.get("https://catfact.ninja/fact")
            if response.status_code != HTTPStatus.OK:
                self.error("Unable to get cat fact")
                context["cat_fact"] = None
            else:
                response_body = json.loads(response.content)
                context["cat_fact"] = response_body["fact"]
        except Exception:
            context["cat_fact"] = None

        return context


class PromoCodeView(TemplateView):
    template_name = "service/promo_codes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tz_info"] = get_tz(self.request.user)
        context["valid_codes"] = PromoCode.objects.filter(is_active=True)
        context["invalid_codes"] = PromoCode.objects.filter(is_active=False)
        return context


class ServiceTypeView(TemplateView):
    template_name = "service/service_types.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tz_info"] = get_tz(self.request.user)
        context["service_types"] = ServiceType.objects.filter()
        return context


class ServiceView(FilterView, ListView):
    model = Service
    template_name = "service/services.html"
    context_object_name = "services"
    filterset_class = ServiceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        context["tz_info"] = get_tz(self.request.user)
        return context


class OrderView(LoginRequiredMixin, ListView):
    model = Order
    login_url = reverse_lazy("login")
    template_name = "orders/orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.request.user.username
        context["tz_info"] = get_tz(self.request.user)
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Order.objects.all()

        elif hasattr(user, "staff_profile"):
            staff = user.staff_profile
            return Order.objects.filter(
                Q(created_by=staff) | Q(assigned_staff=staff)
            ).distinct()

        elif hasattr(user, "client_profile"):
            client = user.client_profile
            return Order.objects.filter(client=client)

        else:
            return Order.objects.none()


class AddOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_create.html"
    success_url = reverse_lazy("orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tz_info"] = get_tz(self.request.user)
        if self.request.POST:
            context["formset"] = OrderItemFormSet(self.request.POST)
        else:
            context["formset"] = OrderItemFormSet(
                queryset=OrderItem.objects.none(),
                instance=self.object
            )
        return context

    def form_valid(self, form):
        if not hasattr(self.request.user, "client_profile"):
            return redirect(reverse_lazy("orders"))

        order = form.save(commit=False)
        order.client = Client.objects.get(user=self.request.user)
        order.status = Order.OrderStatus.PENDING
        order.payment_status = Order.PaymentStatus.UNPAID
        order.save()

        formset = OrderItemFormSet(
            self.request.POST,
            instance=order
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    instance.price_at_order = instance.service.price
                instance.save()
            return super().form_valid(form)
        else:
            order.delete()
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class UpdateOrderView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_create.html"
    success_url = reverse_lazy("orders")
    pk_url_kwarg = "order_id"

    def test_func(self):
        return self.get_object().client.user == self.request.user or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = OrderItemFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context["formset"] = OrderItemFormSet(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        order = form.save(commit=False)

        order.save()

        formset = OrderItemFormSet(
            self.request.POST,
            instance=order
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    instance.price_at_order = instance.service.price
                instance.save()
            formset.save_m2m()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class DeleteOrderView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = "orders/confirm_order_deletion.html"
    success_url = reverse_lazy("orders")
    pk_url_kwarg = "order_id"

    def test_func(self):
        return self.get_object().client.user == self.request.user or self.request.user.is_superuser
