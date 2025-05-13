from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from cleaning_service.models import Client

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Used for password reset.")
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    name = forms.CharField(
        max_length=200,
        required=True,
        help_text="Customer name or Company name"
    )
    contact_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="Primary contact number"
    )
    client_type = forms.ChoiceField(
        choices=Client.ClientType.choices,
        initial=Client.ClientType.PRIVATE
    )
    timezone = forms.CharField(
        max_length=30,
        required=True,
        help_text="Timezone"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()

        client = Client.objects.get(user=user)
        client.name = self.cleaned_data["name"]
        client.contact_number = self.cleaned_data["contact_number"]
        client.client_type = self.cleaned_data["client_type"]
        client.email = self.cleaned_data["email"]
        client.timezone = self.cleaned_data["timezone"]
        client.save()

        client.save()

        user = client.user
        user.email = client.email
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        return user
