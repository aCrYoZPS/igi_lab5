from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from globals.utils import get_tz
from .models import Review
from .forms import ReviewForm


class ReviewView(TemplateView):
    template_name = "service/reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.order_by("publication_date")
        context["tz_info"] = get_tz(self.request.user)
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    template_name = "service/review_form.html"
    success_url = reverse_lazy("reviews")
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "service/review_form.html"
    success_url = reverse_lazy("reviews")
    form_class = ReviewForm
    model = Review

    def test_func(self):
        return self.get_object().author == self.request.user


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "service/confirm_review_deletion.html"
    success_url = reverse_lazy("reviews")

    def test_func(self):
        return self.get_object().author == self.request.user
