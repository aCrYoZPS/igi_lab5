import pytz
from django import forms
from cleaning_service.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'client_type',
            'contact_person',
            'contact_number',
            'email',
            'address',
            'timezone'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter full address'}),
            'contact_number': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'timezone': forms.Select(choices=[(tz, tz) for tz in pytz.common_timezones])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_person'].required = False

        if self.instance and self.instance.pk:
            if self.instance.client_type == Client.ClientType.COMPANY:
                self.fields['contact_person'].required = True

    def clean(self):
        cleaned_data = super().clean()
        client_type = cleaned_data.get('client_type')
        contact_person = cleaned_data.get('contact_person')

        if client_type == Client.ClientType.COMPANY and not contact_person:
            self.add_error('contact_person', 'Contact person is required for companies')

        return cleaned_data
