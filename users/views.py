from django.shortcuts import render, redirect
from django.contrib.auth import login
from cleaning_service import settings
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, settings.AUTHENTICATION_BACKENDS[0])
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
