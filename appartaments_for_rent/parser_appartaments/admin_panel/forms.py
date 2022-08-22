from dataclasses import fields
from django import forms

from .models import Appartament

# Creating a form for admin model

class AppartamentForm(forms.ModelForm):
    """Форма на основе существующией модели"""

    class Meta:
        model = Appartament
        fields = ('title', 'price', 'url')
        widgets = {
            "title" : forms.TextInput,
        } 