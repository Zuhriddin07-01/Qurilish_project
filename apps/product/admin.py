from django.contrib import admin
from .models import Product, ProductImage, ProductComment, ProductRating

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductComment)
admin.site.register(ProductRating)

# Register your models here.
