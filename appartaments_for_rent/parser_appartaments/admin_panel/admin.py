from django.contrib import admin
from django import forms
from .forms import ApartmentForm
from .models import Apartment


@admin.register(Apartment)
class Apartment(admin.ModelAdmin):
    list_display = ("title", "price", "date", "url",)
    form = ApartmentForm
    list_filter = ("date", "price", )

    