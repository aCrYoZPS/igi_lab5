from django.db import models
from django.conf import settings


class Article(models.Model):
    """Represents an article"""
    title = models.CharField(max_length=256)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.URLField(blank=True, null=True)
    summary = models.CharField(max_length=1024, default="")
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {str(self.author)}. Published on {self.publication_date.strftime("%d/%m/%Y %H:%M:%S")}"
