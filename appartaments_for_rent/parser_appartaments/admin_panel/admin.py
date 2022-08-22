from django.contrib import admin
from .forms import AppartamentForm
from .models import Appartament

# Register your models here.

@admin.register(Appartament)
class Appartment(admin.ModelAdmin):
    list_display =  ("title", "price", "date", "url")
    form = AppartamentForm
    list_filter = ("date", "price")

    