# apps/product/serializers.py
from rest_framework import serializers
from .models import Product, ProductImage, ProductComment, ProductRating 


 
 
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_cover', 'uploaded_at']
 
 
class ProductCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
 
    class Meta:
        model = ProductComment
        fields = ['id', 'user_name', 'text', 'created_at']
        read_only_fields = ['user_name', 'created_at']
 
 
class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['id', 'rating']
 
 
class ProductSerializer(serializers.ModelSerializer):
    images       = ProductImageSerializer(many=True, read_only=True)
    comments     = ProductCommentSerializer(many=True, read_only=True)
    builder_name = serializers.CharField(source='builder.get_full_name', read_only=True)
    avg_rating   = serializers.SerializerMethodField()
 
    class Meta:
        model = Product
        fields = [
            'id', 'builder', 'builder_name', 'title', 'description',
            'price', 'price_type', 'duration_days',
            'is_active', 'images', 'comments', 'avg_rating', 'created_at'
        ]
        read_only_fields = ['builder', 'created_at']
 
    def get_avg_rating(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.rating for r in ratings) / ratings.count(), 1)