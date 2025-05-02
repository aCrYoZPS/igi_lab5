from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Article


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "service/article.html", {"article": article})


class ArticlesView(TemplateView):
    template_name = "service/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.order_by("publication_date").reverse()
        return context
