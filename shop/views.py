from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    latest_products = Product.objects.filter(is_active=True)[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'latest_products': latest_products,
    }
    return render(request, 'home.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'category_detail.html', context)
