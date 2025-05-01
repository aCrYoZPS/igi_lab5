from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import Article
from .models import FAQ, Vacancy, About, PrivacyPolicy

import json
import requests


def index(request):
    response = json.loads(requests.get("https://api.ipify.org?format=json").content)
    return render(request, "service/index.html", {"articles": Article.objects.all(), "ip": response["ip"]})


def privacy_policy(request):
    return render(request, "service/privacy_policy.html", {"policy": PrivacyPolicy.objects.last()})


def faq(request):
    return render(request, "service/faq.html", {"faqs": FAQ.objects.all()})


def vacancies(request):
    return render(request, "service/vacancies.html", {"vacancies": Vacancy.objects.all()})


def about(request):
    return render(request, "service/about.html", {"about": About.objects.last()})


class CatFactView(TemplateView):
    template_name = "service/cat_fact.html"

    def get_context_data(self, **kwargs):
        response = json.loads(requests.get("https://catfact.ninja/fact").content)
        context = super().get_context_data(**kwargs)
        context["cat_fact"] = response["fact"]
        return context
