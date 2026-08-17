from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<slug:slug>/', views.category_detail, name='category_detail'),
]
