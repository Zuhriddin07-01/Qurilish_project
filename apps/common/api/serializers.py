 
from rest_framework import serializers
from django.contrib.auth import get_user_model
 
User = get_user_model()
 
 
class WorkerListSerializer(serializers.ModelSerializer):
    full_name    = serializers.CharField(source='get_full_name')
    avg_rating   = serializers.FloatField(read_only=True)
    total_orders = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'phone',   
            'address', 'avg_rating', 'total_orders'
        ]
 
 
class WorkerDetailSerializer(serializers.ModelSerializer):
    """Bitta quruvchi profili — to'liq ma'lumot"""
    full_name = serializers.CharField(source='get_full_name')
 
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'avatar', 'phone',
            'address', 'bio', 'created_at'
        ]
 
 
class WorkPhotoSerializer(serializers.Serializer):
    """Quruvchi yuklagan ish rasmlari"""
    id          = serializers.IntegerField(read_only=True)
    image       = serializers.ImageField()
    caption     = serializers.CharField(max_length=200, required=False, allow_blank=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
 
 
class ReviewSerializer(serializers.Serializer):
    """Sharh yozish va ko'rish"""
    id          = serializers.IntegerField(read_only=True)
    client_name = serializers.CharField(read_only=True)
    rating      = serializers.IntegerField(min_value=1, max_value=5)
    comment     = serializers.CharField()
    created_at  = serializers.DateTimeField(read_only=True)
