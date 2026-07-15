from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
 
User = get_user_model()
 
 
class RegisterSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish"""
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
 
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password', 'password2']
 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Parollar mos kelmadi!'})
        return attrs
 
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
 
 
class LoginSerializer(serializers.Serializer):
    """Tizimga kirish"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
 
 
class UserProfileSerializer(serializers.ModelSerializer):
    """Foydalanuvchi profili"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
 
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'first_name', 'last_name',
            'email', 'phone', 'avatar', 'address', 'bio', 'role', 'created_at'
        ]
        read_only_fields = ['id', 'username', 'role', 'created_at']
 
 
class ChangePasswordSerializer(serializers.Serializer):
    """Parol o'zgartirish"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)
 
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Yangi parollar mos kelmadi!'})
        return attrs