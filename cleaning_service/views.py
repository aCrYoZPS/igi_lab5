from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import Article
from .models import FAQ, Vacancy, About, PrivacyPolicy, PromoCode
from globals.logging import LoggingMixin

import json
import requests
from http import HTTPStatus


def index(request):
    response = json.loads(requests.get("https://api.ipify.org?format=json").content)
    return render(request, "service/index.html", {"article": Article.objects.last(), "ip": response["ip"]})


def privacy_policy(request):
    return render(request, "service/privacy_policy.html", {"policy": PrivacyPolicy.objects.last()})


def faq(request):
    return render(request, "service/faq.html", {"faqs": FAQ.objects.all()})


def vacancies(request):
    return render(request, "service/vacancies.html", {"vacancies": Vacancy.objects.all()})


def about(request):
    return render(request, "service/about.html", {"about": About.objects.last()})


class CatFactView(TemplateView, LoggingMixin):
    template_name = "service/cat_fact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get("https://catfact.ninja/fact")
        if response.status_code != HTTPStatus.OK:
            self.error("Unable to get cat fact")
            context["cat_fact"] = None
        else:
            response_body = json.loads(response.content)
            context["cat_fact"] = response_body["fact"]
        return context


class PromoCodeView(TemplateView):
    template_name = "service/promo_codes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["valid_codes"] = PromoCode.objects.filter(is_active=True)
        context["invalid_codes"] = PromoCode.objects.filter(is_active=False)
        return context
