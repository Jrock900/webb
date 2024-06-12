from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('clothes/<int:pk>/', views.clothes, name='clothes'),
    path('category/<slug:nme>', views.category, name='category'),
    path('search_results/', views.search_results, name='search_results'),

    
]