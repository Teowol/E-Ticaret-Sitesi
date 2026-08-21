from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Brand, Category
from django.utils.translation import gettext_lazy as _


class SellerRegistrationForm(UserCreationForm):
    store_name = forms.CharField(
        label="Mağaza Adı",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Mağaza adınızı girin",
        }),
    )

    phone = forms.CharField(
        label="Telefon",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Telefon numaranızı girin",
        }),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kullanıcı adınızı girin",
                "autocomplete": "username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "E-posta adresinizi girin",
                "autocomplete": "email",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Şifrenizi girin",
            "autocomplete": "new-password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Şifrenizi tekrar girin",
            "autocomplete": "new-password",
        })

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            user.profile.is_seller = True
            user.profile.store_name = self.cleaned_data.get("store_name")
            user.profile.phone = self.cleaned_data.get("phone")
            user.profile.save()

        return user


class ProductForm(forms.ModelForm):
    new_brand = forms.CharField(
        label="Yeni marka ekle",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Listede yoksa yeni marka adı yazın",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Product
        fields = [
            "category", "brand", "name", "slug", "description",
            "price", "discount_price", "stock", "image",
            "is_featured", "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Yeni marka girilebileceği için mevcut marka alanı zorunlu olmamalı.
        self.fields["brand"].required = False

        self.fields["brand"].widget.attrs.update({
            "class": "form-select",
        })

        self.fields["category"].widget.attrs.update({
            "class": "form-select",
        })

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")
        brand = cleaned_data.get("brand")
        new_brand = cleaned_data.get("new_brand")

        # Ne mevcut marka ne de yeni marka seçilmişse hata ver.
        if not brand and not new_brand:
            self.add_error(
                "brand",
                "Lütfen mevcut bir marka seçin veya yeni marka adı yazın."
            )

        # Mevcut marka seçildiyse kategoriyle eşleşmesini kontrol et.
        if category and brand and not new_brand:
            is_brand_in_category = brand.categories.filter(
                pk=category.pk
            ).exists()

            if not is_brand_in_category:
                self.add_error(
                    "brand",
                    "Seçtiğiniz marka, seçilen kategoriye bağlı değil."
                )

        return cleaned_data
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        labels = {
            "name": _("Kategori Adı"),
            "slug": _("URL"),
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Kategori adı"),
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("kategori-adi"),
            }),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "categories"]
        labels = {
            "name": _("Marka Adı"),
            "categories": _("İlgili Kategoriler"),
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Marka adı"),
            }),
            "categories": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }