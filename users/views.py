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
            redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
            return redirect(redirect_url)
        else:
            # Form is invalid, re-render the page with the form and errors
            # The form instance now contains error messages
            pass
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
