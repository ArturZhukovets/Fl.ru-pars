from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Apartment


class ApartmentsView(ListView):
    model = Apartment
    template_name = 'admin_panel/apartment_list.html'
    queryset = Apartment.objects.all().order_by('-date')[:50]

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['obj'] = Apartment.objects.all()
    #     return context

