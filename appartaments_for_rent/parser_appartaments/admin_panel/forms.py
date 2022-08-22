from dataclasses import fields
from django import forms

from .models import Apartment

# Creating a form for admin model

class AppartamentForm(forms.ModelForm):
    """Форма на основе существующией модели"""

    class Meta:
        model = Apartment
        fields = ('title', 'price', 'url')
        widgets = {
            "title" : forms.TextInput,
        } 