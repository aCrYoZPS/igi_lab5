from django.shortcuts import render, redirect
from django.contrib.auth import login
from . import settings
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
