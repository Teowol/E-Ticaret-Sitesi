from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<slug:slug>/', views.product_list_by_category, name='category_detail'),
    path('urun/<slug:slug>/', views.product_detail, name='product_detail'),
    path('sepet/', views.cart_detail, name='cart_detail'),
    path('sepet/ekle/<int:product_id>/', views.cart_add, name='cart_add'),
    path('sepet/kaldir/<int:product_id>/', views.cart_remove, name='cart_remove'),
]