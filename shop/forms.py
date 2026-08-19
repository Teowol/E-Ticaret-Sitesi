from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Brand, Category


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
        label="Yeni Marka (listede yoksa buraya yazın)",
        max_length=100,
        required=False,
        help_text="Marka listede yoksa bu alana yeni marka adını yazın, otomatik olarak eklenir."
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
        self.fields["brand"].required = False

    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get("brand")
        new_brand = cleaned_data.get("new_brand")

        if not brand and not new_brand:
            raise forms.ValidationError("Lütfen bir marka seçin veya yeni marka adı girin.")

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kategori adı",
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "kategori-adi",
            }),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "categories"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Marka adı",
            }),
            "categories": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }