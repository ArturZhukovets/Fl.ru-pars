from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Apartment


class ApartmentsView(ListView):
    model = Apartment
    template_name = 'admin_panel/apartment_list.html'
    paginate_by = 20


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        x = 0
        return context

