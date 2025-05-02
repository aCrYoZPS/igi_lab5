from django.views.generic import TemplateView
from .models import Review


class ReviewView(TemplateView):
    template_name = "service/reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.all()
        return context
