from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_name',
            'title', 'description', 'address',
            'budget', 'status', 'created_at'
        ]
        read_only_fields = ['client', 'status', 'created_at']