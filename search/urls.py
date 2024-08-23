from django.urls import path
from .views import search_nutrition, search_foods, home_view, login_view, logout_view, register_view, custom_404_view


urlpatterns = [
    path('dashboard/', home_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('search/', search_foods, name='search_foods'),
    path('nutrition/', search_nutrition, name='search_nutrition'),
]