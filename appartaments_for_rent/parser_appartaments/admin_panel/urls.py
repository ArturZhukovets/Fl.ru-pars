from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ApartmentsView.as_view(), name='apartment_list'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('<int:pk>/', views.AddToFavorite.as_view(), name='add_to_favorite'),
    path('favorite/', views.UserFavorite.as_view(), name='favorite'),
    path('favorite/del<int:pk>', views.del_from_favorite, name='del_from_fav'),




]