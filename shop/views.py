from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Category, Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import SellerRegistrationForm, ProductForm

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


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Hesabınız başarıyla oluşturuldu! Hoş geldiniz.'))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Başarıyla giriş yaptınız.'))
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        messages.error(request, _('Kullanıcı adı veya şifre hatalı.'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, _('Çıkış yapıldı.'))
    return redirect('home')

def is_seller(user):
    return hasattr(user, 'profile') and user.profile.is_seller


def seller_register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Satıcı hesabınız oluşturuldu! Artık ürün ekleyebilirsiniz.')
            return redirect('seller_dashboard')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/seller_register.html', {'form': form})


@login_required
def seller_dashboard(request):
    if not is_seller(request.user):
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
        return redirect('home')
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller/dashboard.html', {'products': products})


@login_required
def seller_product_add(request):
    if not is_seller(request.user):
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Ürün başarıyla eklendi.')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Ürün Ekle'})


@login_required
def seller_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün güncellendi.')
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Ürünü Düzenle'})


@login_required
def seller_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Ürün silindi.')
    return redirect('seller_dashboard')