from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

from .models import Apartment

# Creating a form for admin model

class ApartmentForm(forms.ModelForm):
    """Форма на основе существующий модели, для админки
    Здесь прописаны поля, для редактирования."""

    class Meta:
        model = Apartment
        fields = ('title', 'price', 'url', 'user_favorite')
        widgets = {
            "title": forms.Textarea,
        }


class ApartmentSearchForm(forms.ModelForm):
    """Форма для поиска"""
    class Meta:
        model = Apartment
        fields = ('title', )



class RegisterUserForm(UserCreationForm):
    """Форма для регистрации. Наследуется от базовой джанговского класса создания форм
     и будет его расширять. Важно, чтобы названия переопределяемых полей совпадали с полями из таблицы."""
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': ' form-input'}))
    password2 = None
    email = forms.CharField(label="Эл. почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    # first_name = forms.CharField(label="Ваше имя (не обязательно)", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User   # Стандартная модель юзеров в Джанго
        fields = ('username', 'password1', 'email')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

