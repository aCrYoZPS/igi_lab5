from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, PromoCode
from django.forms import BaseInlineFormSet


class RequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        has_service = False
        for form in self.forms:
            if form.cleaned_data.get('service'):
                has_service = True
                break

        if not has_service:
            raise forms.ValidationError("You must select at least one service")


class OrderForm(forms.ModelForm):
    promo_code = forms.ModelChoiceField(
        queryset=PromoCode.objects.filter(is_active=True),
        required=False,
        help_text="Apply promocode (optional)"
    )

    def clean_promo_code(self):
        code = self.cleaned_data.get("promo_code")
        if code and not code.is_active:
            raise forms.ValidationError("This promo code is expired or invalid")
        return code

    class Meta:
        model = Order
        fields = ["address", "work_date", "promo_code"]
        widgets = {
            "work_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    formset=RequiredInlineFormSet,
    fields=("service", "quantity"),
    extra=3,
    can_delete=False,
    min_num=1,
    validate_min=True,
    widgets={
        "service": forms.Select(attrs={"class": "service-select"}),
        "quantity": forms.NumberInput(attrs={"min": 1})
    }
)
