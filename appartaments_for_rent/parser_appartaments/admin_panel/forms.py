from dataclasses import fields
from django import forms

from .models import Apartment

# Creating a form for admin model

class ApartmentForm(forms.ModelForm):
    """Форма на основе существующий модели, для админки"""

    class Meta:
        model = Apartment
        fields = ('title', 'price', 'url')
        widgets = {
            "title": forms.TextInput,
        }


class ApartmentSearchForm(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = ('title', )

