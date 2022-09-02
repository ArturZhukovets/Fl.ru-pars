from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Apartment


class ApartmentsView(ListView):
    model = Apartment
    # template_name = 'admin_panel/apartment_list.html'
    paginate_by = 20


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        x = 0
        return context


class ApartmentsFilter(ListView):
    model = Apartment
    template_name = 'admin_panel/apartment_list_filter.html'

    def get_queryset(self):
        """Определяет queryset в зависимости от get_запроса"""
        if self.request.GET.get('search', False):
            queryset = Apartment.objects.filter(title__icontains=self.request.GET['search'])
            return queryset

        elif self.request.GET.get('sort', False) == 'date':
            queryset = Apartment.objects.order_by('-date')
            return queryset
        elif self.request.GET.get('sort', False) == 'price_u':
            queryset = Apartment.objects.order_by('price')
            return queryset
        elif self.request.GET.get('sort', False) == 'price_d':
            queryset = Apartment.objects.order_by('-price')
            return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if self.request.GET.get('search'):
            context['value'] = self.request.GET['search']
        return context



