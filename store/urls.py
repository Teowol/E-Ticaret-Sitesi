from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('urun/<slug:slug>/', views.product_detail, name='product_detail'),
]