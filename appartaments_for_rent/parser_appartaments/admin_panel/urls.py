from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ApartmentsView.as_view(), name='apartment_list'),
    path('filter/', views.ApartmentsFilter.as_view(), name='filter'),
    path('login/', views.ApartmentsFilter.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),



]