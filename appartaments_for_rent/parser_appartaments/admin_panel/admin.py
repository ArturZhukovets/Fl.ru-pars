from django.contrib import admin
from .forms import ApartmentForm
from .models import Apartment

# Register your models here.

@admin.register(Apartment)
class Apartment(admin.ModelAdmin):
    list_display = ("title", "price", "date", "url")
    form = ApartmentForm
    list_filter = ("date", "price")

    