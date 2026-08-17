from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField("Kategori Adı", max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField("Marka", max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField("Ürün Adı", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Açıklama", blank=True)
    price = models.DecimalField("Fiyat", max_digits=10, decimal_places=2)
    discount_price = models.DecimalField("İndirimli Fiyat", max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField("Stok", default=0)
    image = models.ImageField("Görsel", upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField("Öne Çıkan", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def discount_percent(self):
        if self.discount_price:
            return int(100 - (self.discount_price / self.price * 100))
        return 0