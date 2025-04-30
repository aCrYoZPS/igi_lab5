from django.shortcuts import render
from .models import Article


def index(request):
    article_info = {}
    for article in Article.objects.all():

    return render(request, "service/index.html")
