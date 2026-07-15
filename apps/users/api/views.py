from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
 
User = get_user_model()
 
 
class RegisterView(APIView):
    """
    POST /api/users/register/
    Yangi foydalanuvchi ro'yxatdan o'tishi
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.get_full_name(),
                    'role': user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class LoginView(APIView):
    """
    POST /api/users/login/
    Tizimga kirish — token qaytaradi
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
 
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Tizimga muvaffaqiyatli kirdingiz!',
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'full_name': user.get_full_name(),
                        'role': user.role,
                    }
                })
            return Response(
                {'error': 'Username yoki parol noto\'g\'ri!'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class LogoutView(APIView):
    """
    POST /api/users/logout/
    Tizimdan chiqish — tokenni o'chiradi
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
 
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Tizimdan chiqdingiz!'})
 
 
class ProfileView(APIView):
    """
    GET   /api/users/profile/  → Profilni ko'rish
    PATCH /api/users/profile/  → Profilni yangilash
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
 
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
 
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil yangilandi!',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class ChangePasswordView(APIView):
    """
    POST /api/users/change-password/
    Parol o'zgartirish
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
 
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
 
            # Eski parolni tekshirish
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': 'Eski parol noto\'g\'ri!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
 
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class AvatarUploadView(APIView):
    """
    POST /api/users/avatar/
    Profil rasmini yuklash
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
 
    def post(self, request):
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response(
                {'error': 'Rasm yuklanmadi!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.avatar = avatar
        request.user.save()
        return Response({'message': 'Profil rasmi yangilandi!'})