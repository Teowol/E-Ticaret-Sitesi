from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product


class SellerRegistrationForm(UserCreationForm):
    store_name = forms.CharField(
        label="Mağaza Adı",
        max_length=150,
        required=True,
    )
    phone = forms.CharField(
        label="Telefon",
        max_length=20,
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.is_seller = True
            user.profile.store_name = self.cleaned_data.get("store_name")
            user.profile.phone = self.cleaned_data.get("phone")
            user.profile.save()
        return user


class ProductForm(forms.ModelForm):
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