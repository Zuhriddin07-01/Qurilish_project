# # apps/product/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, ProductComment, ProductRating  # ← import
from .serializers import (                                   # ← import
    ProductSerializer,
    ProductCommentSerializer,
    ProductRatingSerializer,
    ProductImageSerializer,
)

# keyin viewlar ...
 
 
class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/products/  → Barcha xizmatlar ro'yxati
    POST /api/products/  → Yangi xizmat yaratish (faqat quruvchi)
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
 
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
 
    def perform_create(self, serializer):
        serializer.save(builder=self.request.user)
 
 
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/products/{id}/  → Bitta xizmat
    PATCH  /api/products/{id}/  → Yangilash (faqat egasi)
    DELETE /api/products/{id}/  → O'chirish (faqat egasi)
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
 
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        if product.builder != request.user:
            return Response({'error': 'Siz bu xizmatni o\'zgartira olmaysiz'}, status=403)
        return super().update(request, *args, **kwargs)
 
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.builder != request.user:
            return Response({'error': 'Siz bu xizmatni o\'chira olmaysiz'}, status=403)
        return super().destroy(request, *args, **kwargs)
 
 
class ProductCommentView(generics.CreateAPIView):
    """
    POST /api/products/{id}/comment/  → Savol yoki sharh qoldirish
    """
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, product=product)
 
 
class ProductRatingView(APIView):
    """
    POST /api/products/{id}/rate/  → Baholash (1-5)
    """
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        rating_value = request.data.get('rating')
 
        if not rating_value or int(rating_value) not in range(1, 6):
            return Response({'error': 'Baho 1 dan 5 gacha bo\'lishi kerak'}, status=400)
 
        rating, created = ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating_value}
        )
        msg = 'Baho qo\'yildi' if created else 'Baho yangilandi'
        return Response({'message': msg, 'rating': rating_value})
 
 
class ProductImageUploadView(generics.CreateAPIView):
    """
    POST /api/products/{id}/images/  → Rasm yuklash
    """
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['pk'])
        if product.builder != self.request.user:
            raise permissions.PermissionDenied('Siz bu xizmatga rasm yuklay olmaysiz')
        serializer.save(product=product)

# Create your views here.
