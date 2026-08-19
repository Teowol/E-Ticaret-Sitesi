from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, Brand, Profile
from .forms import SellerRegistrationForm, ProductForm, CategoryForm, BrandForm
from django.db import models
from django.contrib.auth.models import User

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
    total_price = 0

    for product_id, quantity in list(cart.items()):
        product = Product.objects.filter(
            pk=product_id,
            is_active=True,
        ).first()

        if product is None:
            cart.pop(product_id, None)
            request.session['cart'] = cart
            request.session.modified = True
            continue

        item_total = product.current_price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': Category.objects.all(),
    })

def cart_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = request.session.get('cart', {})

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        quantity = max(quantity, 1)
        current_quantity = cart.get(str(product.id), 0)
        new_quantity = current_quantity + quantity

        if product.stock <= 0:
            messages.warning(request, f"{product.name} stokta yok.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        if new_quantity > product.stock:
            new_quantity = product.stock
            messages.warning(
                request,
                f"{product.name} için stoktaki maksimum adede ulaşıldı."
            )
        else:
            messages.success(request, f"{product.name} sepete eklendi.")

        cart[str(product.id)] = new_quantity
        request.session['cart'] = cart
        request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_update(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = request.session.get('cart', {})

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            cart.pop(str(product.id), None)
            messages.info(request, f"{product.name} sepetten kaldırıldı.")
        elif quantity > product.stock:
            cart[str(product.id)] = product.stock
            messages.warning(
                request,
                f"{product.name} için stoktaki maksimum adet uygulandı."
            )
        else:
            cart[str(product.id)] = quantity
            messages.success(request, "Sepet güncellendi.")

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')

def cart_remove(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart.pop(str(product_id))
            request.session['cart'] = cart
            request.session.modified = True
            messages.info(request, "Ürün sepetten kaldırıldı.")

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

            new_brand_name = form.cleaned_data.get('new_brand')
            category = form.cleaned_data.get('category')

            if new_brand_name:
                brand, created = Brand.objects.get_or_create(
                    name__iexact=new_brand_name,
                    defaults={'name': new_brand_name}
                )
                if category:
                    brand.categories.add(category)
                product.brand = brand

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
            product = form.save(commit=False)

            new_brand_name = form.cleaned_data.get('new_brand')
            category = form.cleaned_data.get('category')

            if new_brand_name:
                brand, created = Brand.objects.get_or_create(
                    name__iexact=new_brand_name,
                    defaults={'name': new_brand_name}
                )
                if category:
                    brand.categories.add(category)
                product.brand = brand

            product.save()
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

def search_results(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.all()

    if query:
        featured_products = Product.objects.filter(
            is_active=True,
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()
    else:
        featured_products = Product.objects.none()

    return render(request, 'search_results.html', {
        'categories': categories,
        'featured_products': featured_products,
        'query': query,
    })

@login_required
@user_passes_test(lambda u: is_seller(u) or u.is_superuser, login_url='/giris/')
def manage_categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'delete_category_id' in request.POST:
            category_id = request.POST.get('delete_category_id')
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            messages.success(request, "Kategori silindi.")
            return redirect('manage_categories')
        else:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Kategori eklendi.")
                return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/manage_categories.html', {
        'categories': categories,
        'form': form,
    })


@login_required
@user_passes_test(lambda u: is_seller(u) or u.is_superuser, login_url='/giris/')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategori güncellendi.")
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/edit_category.html', {'form': form, 'category': category})


@login_required
@user_passes_test(lambda u: is_seller(u) or u.is_superuser, login_url='/giris/')
def manage_brands(request):
    brands = Brand.objects.all()
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Marka eklendi.")
            return redirect('manage_brands')
    else:
        form = BrandForm()
    return render(request, 'admin_panel/manage_brands.html', {
        'brands': brands,
        'form': form,
    })


@login_required
@user_passes_test(lambda u: is_seller(u) or u.is_superuser, login_url='/giris/')
def edit_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Marka güncellendi.")
            return redirect('manage_brands')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'admin_panel/edit_brand.html', {'form': form, 'brand': brand})

def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_sellers': Profile.objects.filter(is_seller=True).count(),
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_brands': Brand.objects.count(),
        'recent_products': Product.objects.order_by('-created_at')[:10],
        'sellers': Profile.objects.filter(is_seller=True).select_related('user'),
    }
    return render(request, 'admin_panel/dashboard.html', context)