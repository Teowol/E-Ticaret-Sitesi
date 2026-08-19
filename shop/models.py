from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField("Kategori Adı", max_length=100)
    slug = models.SlugField("URL", unique=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField("Marka Adı", max_length=100)
    categories = models.ManyToManyField(
        Category,
        related_name="brands",
        verbose_name="İlgili Kategoriler",
        blank=True,
    )

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Kategori",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seller_products",
        verbose_name="Satıcı",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Marka",
    )
    name = models.CharField("Ürün Adı", max_length=200)
    slug = models.SlugField("URL", unique=True)
    description = models.TextField("Açıklama", blank=True)
    price = models.DecimalField("Normal Fiyat", max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        "İndirimli Fiyat",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    stock = models.PositiveIntegerField("Stok", default=0)
    image = models.ImageField(
        "Ürün Görseli",
        upload_to="products/",
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField("Öne Çıkan", default=False)
    is_active = models.BooleanField("Aktif", default=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)


    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def current_price(self):
        return self.discount_price or self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price:
            return int(100 - (self.discount_price / self.price * 100))
        return 0

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    is_seller = models.BooleanField("Satıcı mı?", default=False)
    store_name = models.CharField("Mağaza Adı", max_length=150, blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    is_approved = models.BooleanField("Onaylı Satıcı", default=False)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()