from django.contrib.auth.models import User
from django.db.models import Count
import base64
import io
import matplotlib.pyplot as plt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import matplotlib
matplotlib.use('Agg')


class StatsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'stats.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.annotate(review_count=Count('review'))
        usernames = [user.username for user in users]
        counts = [user.review_count for user in users]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(usernames, counts)
        plt.xlabel('Users')
        plt.ylabel('Number of Reviews')
        plt.title('User Review Statistics')
        plt.xticks(rotation=45, ha='right')  # Rotate labels for readability

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}',
                     ha='center', va='bottom')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        context['chart_image'] = image_base64
        return context
