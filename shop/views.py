from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, is_active=True)
    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })


def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': products,
        'selected_category': category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'product_detail.html', {
        'product': product,
        'categories': Category.objects.all(),
    })


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': product.current_price * quantity,
        })
    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'categories': Category.objects.all(),
    })


def cart_add(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        cart[str(product.id)] = min(quantity, product.stock or quantity)
        request.session['cart'] = cart
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_detail')