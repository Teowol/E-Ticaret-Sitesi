from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<slug:slug>/', views.product_list_by_category, name='category_detail'),
    path('urun/<slug:slug>/', views.product_detail, name='product_detail'),
    path('sepet/', views.cart_detail, name='cart_detail'),
    path('sepet/ekle/<int:product_id>/', views.cart_add, name='cart_add'),
    path('sepet/guncelle/<int:product_id>/', views.cart_update, name='cart_update'),
    path('sepet/kaldir/<int:product_id>/', views.cart_remove, name='cart_remove'),

    path('kayit/', views.register_view, name='register'),
    path('giris/', views.login_view, name='login'),
    path('cikis/', views.logout_view, name='logout'),

    path('satici/kayit/', views.seller_register_view, name='seller_register'),
    path('satici/panel/', views.seller_dashboard, name='seller_dashboard'),
    path('satici/urun-ekle/', views.seller_product_add, name='seller_product_add'),
    path('satici/urun/<int:pk>/duzenle/', views.seller_product_edit, name='seller_product_edit'),
    path('satici/urun/<int:pk>/sil/', views.seller_product_delete, name='seller_product_delete'),

    path('arama/', views.search_results, name='search_results'),

    path('satici/kategoriler/', views.manage_categories, name='manage_categories'),
    path('satici/kategoriler/<int:pk>/duzenle/', views.edit_category, name='edit_category'),
    path('satici/markalar/', views.manage_brands, name='manage_brands'),
    path('satici/markalar/<int:pk>/duzenle/', views.edit_brand, name='edit_brand'),

    path('yonetim-panelim/', views.admin_dashboard, name='admin_dashboard'),
]