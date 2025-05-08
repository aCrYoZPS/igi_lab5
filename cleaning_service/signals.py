from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client


@receiver(post_save, sender=User)
def handle_client_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.get_or_create(user=instance)
