
# apps/product/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# keyin modellar ...
 
 
class Product(models.Model):
    """Quruvchi taklif qiladigan xizmat"""
 
    class PriceType(models.TextChoices):
        PER_SQM    = 'per_sqm',  'm² uchun'
        PER_DAY    = 'per_day',  'Kunlik'
        FIXED      = 'fixed',    'Belgilangan'
        NEGOTIABLE = 'neg',      'Kelishiladi'
 
    builder      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title        = models.CharField(max_length=200, verbose_name='Xizmat nomi')
    description  = models.TextField(verbose_name='Tavsif / Maslahat')
    price        = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_type   = models.CharField(max_length=10, choices=PriceType.choices, default=PriceType.NEGOTIABLE)
    duration_days = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ish vaqti (kun)')
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.title} — {self.builder.get_full_name()}"
 
    class Meta:
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'
        ordering = ['-created_at']
 
 
class ProductImage(models.Model):
    """Xizmat rasmlari"""
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image      = models.ImageField(upload_to='products/%Y/%m/')
    is_cover   = models.BooleanField(default=False, verbose_name='Muqova')
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.product.title} rasmi"
 
 
class ProductComment(models.Model):
    """Foydalanuvchi savoli / sharhi"""
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments')
    text       = models.TextField(verbose_name='Savol yoki sharh')
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.user.get_full_name()}: {self.text[:50]}"
 
    class Meta:
        ordering = ['-created_at']
 
 
class ProductRating(models.Model):
    """Foydalanuvchi baholashi (1-5)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_ratings')
    rating  = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        unique_together = ('product', 'user')  # bir user bir marta baholaydi
 
    def __str__(self):
        return f"{self.product.title} — {self.rating}⭐"

# Create your models here.
