# apps/product/urls.py
from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductCommentView,
    ProductRatingView,
    ProductImageUploadView,
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/comment/', ProductCommentView.as_view(), name='product-comment'),
    path('products/<int:pk>/rate/', ProductRatingView.as_view(), name='product-rate'),
    path('products/<int:pk>/images/', ProductImageUploadView.as_view(), name='product-images'),
]