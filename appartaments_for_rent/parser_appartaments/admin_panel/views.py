from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import login, logout

from .forms import RegisterUserForm, LoginUserForm
from .models import Apartment


class ApartmentsView(ListView):
    model = Apartment
    # template_name = 'admin_panel/apartment_list.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

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
        else:
            queryset = super().get_queryset()
            return queryset

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'admin_panel/register.html'
    success_url = reverse_lazy('apartment_list')     # При успешной заполнении формы регистрации перенаправляет

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


def login_user(request):
    """Вход пользователя. Если форма валидна (и пользователь есть в базе)
    функцией login логиним юзера, данные которого взяты из формы"""
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        else:
            messages.error(request, "Неправильно введен логин или пароль. Попробуйте ещё раз")
            return render(request, 'admin_panel/login.html', {'form': form})
    else:
        form = LoginUserForm()
        return render(request, 'admin_panel/login.html', {'form':form})
    return redirect('apartment_list')


def logout_user(request):
    """Логаут"""
    logout(request)
    return redirect('apartment_list')


class UserFavorite(ListView):
    model = Apartment
    template_name = 'admin_panel/user_favorite.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = self.request.user.apartment_set

        """Определяет queryset в зависимости от get_запроса"""
        if self.request.GET.get('search', False):
            queryset = queryset.filter(title__icontains=self.request.GET['search'])

        elif self.request.GET.get('sort', False) == 'date':
            queryset = queryset.order_by('-date')

        elif self.request.GET.get('sort', False) == 'price_u':
            queryset = queryset.order_by('price')

        elif self.request.GET.get('sort', False) == 'price_d':
            queryset = queryset.order_by('-price')

        else:
            queryset = queryset.all()
        return queryset


class AddToFavorite(View):
    """При нажатии на кнопку формируется пост запрос.
    Форму на валидность проверять не нужно, просто указанную квартиру добавляем актуальному юзеру"""
    def post(self, request, pk:int):
        apartment = Apartment.objects.get(id=int(pk))
        apartment.user_favorite.add(self.request.user)
        # self.request.user.apartment_set.add(apartment)
        return redirect('apartment_list')



def del_from_favorite(request, pk):
    """
    Пока только таким путём. По pk Берём объект модели Apartment,
    находим всех привязанных к нему юзеров и удаляем юзера с аккаунта которого идёт запрос.
    """
    if request.method == "POST":
        Apartment.objects.get(id=pk).user_favorite.remove(request.user)
        return redirect('favorite')