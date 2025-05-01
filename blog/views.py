from django.shortcuts import render, get_object_or_404
from .models import Article


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "service/article.html", {"article": article})
