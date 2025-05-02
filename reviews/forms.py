from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "content", "score"]
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
                'class': 'form-control'
            })
        }
