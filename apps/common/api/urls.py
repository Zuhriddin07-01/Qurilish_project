
from django.urls import path
from . import views
 
urlpatterns = [
    # Quruvchilar ro'yxati (filter, qidirish)
    path('workers/', views.WorkerListView.as_view(), name='worker-list'),
 
    # Bitta quruvchi profili
    path('workers/<int:pk>/', views.WorkerDetailView.as_view(), name='worker-detail'),
 
    # Quruvchi ish rasmlari
    path('workers/<int:pk>/photos/', views.WorkerPhotosView.as_view(), name='worker-photos'),
 
    # Sharh ro'yxati va qoldirish
    path('workers/<int:pk>/reviews/', views.ReviewListCreateView.as_view(), name='worker-reviews'),
 
    # Rasm yuklash (quruvchi uchun)
    path('photos/upload/', views.WorkPhotoUploadView.as_view(), name='photo-upload'),
]

