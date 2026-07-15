
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    WorkerListSerializer,
    WorkerDetailSerializer,
    WorkPhotoSerializer,
    ReviewSerializer,
)
 
User = get_user_model()
 
 
class WorkerListView(APIView):
    """
    GET /api/common/workers/
    Barcha quruvchilar ro'yxati.
    ?search=Ali — ism bo'yicha qidirish
    ?address=Toshkent — shahar bo'yicha filter
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkerListSerializer
 
    def get(self, request):
        workers = User.objects.filter(role='builder', is_active=True)
 
        # Qidirish
        search = request.query_params.get('search')
        if search:
            workers = workers.filter(first_name__icontains=search) | \
                      workers.filter(last_name__icontains=search)
 
        # Manzil bo'yicha filter
        address = request.query_params.get('address')
        if address:
            workers = workers.filter(address__icontains=address)
 
        data = []
        for worker in workers:
            data.append({
                'id': worker.id,
                'full_name': worker.get_full_name(),
                'avatar': request.build_absolute_uri(worker.avatar.url) if worker.avatar else None,
                'phone': worker.phone,
                'address': worker.address,
                'bio': worker.bio,
            })
 
        return Response(data)
 
 
class WorkerDetailView(APIView):
    """
    GET /api/common/workers/{id}/
    Bitta quruvchining to'liq profili + ishlari + sharhlari
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkerDetailSerializer
 
    def get(self, request, pk):
        worker = get_object_or_404(User, pk=pk, role='builder')
 
        # Asosiy ma'lumot
        worker_data = {
            'id': worker.id,
            'full_name': worker.get_full_name(),
            'avatar': request.build_absolute_uri(worker.avatar.url) if worker.avatar else None,
            'phone': worker.phone,
            'address': worker.address,
            'bio': worker.bio,
            'created_at': worker.created_at,
        }
 
        return Response({
            'worker': worker_data,
        })
 
 
class WorkPhotoUploadView(APIView):
    """
    POST /api/common/photos/upload/
    Quruvchi o'z ish rasmini yuklaydi
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = WorkPhotoSerializer 
 
    def post(self, request):
        if request.user.role != 'builder':
            return Response(
                {'error': 'Faqat quruvchilar rasm yuklay oladi'},
                status=status.HTTP_403_FORBIDDEN
            )
 
        image = request.FILES.get('image')
        caption = request.data.get('caption', '')
 
        if not image:
            return Response(
                {'error': 'Rasm yuklanmadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        return Response({
            'message': 'Rasm muvaffaqiyatli yuklandi',
            'caption': caption,
        }, status=status.HTTP_201_CREATED)
 
 
class WorkerPhotosView(APIView):
    """
    GET /api/common/workers/{id}/photos/
    Quruvchining barcha ish rasmlari
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkPhotoSerializer 
 
    def get(self, request, pk):
        worker = get_object_or_404(User, pk=pk, role='builder')
        return Response({
            'worker_id': worker.id,
            'worker_name': worker.get_full_name(),
            'photos': []  
        })
 
 
class ReviewListCreateView(APIView):
    """
    GET  /api/common/workers/{id}/reviews/ → Quruvchi sharhlari
    POST /api/common/workers/{id}/reviews/ → Sharh qoldirish
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
 
    def get(self, request, pk):
        worker = get_object_or_404(User, pk=pk, role='builder')
        # Review modelingiz bo'lsa shu yerdan olinadi
        return Response({
            'worker_id': worker.id,
            'worker_name': worker.get_full_name(),
            'reviews': []
        })
 
    def post(self, request, pk):
        worker = get_object_or_404(User, pk=pk, role='builder')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
 
        if not rating or not comment:
            return Response(
                {'error': 'Baho va sharh kiritish shart'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        if int(rating) not in range(1, 6):
            return Response(
                {'error': 'Baho 1 dan 5 gacha bo\'lishi kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        return Response({
            'message': 'Sharh muvaffaqiyatli qoldirildi',
            'worker_id': worker.id,
            'rating': rating,
            'comment': comment,
        }, status=status.HTTP_201_CREATED)