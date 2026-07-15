# apps/common/urls.py
from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    # Asosiy sahifa
    path('', views.worker_list, name='home'),
    
    # Ishchi profili
    path('create-profile/', views.create_worker_profile, name='create_worker_profile'),
    path('dashboard/', views.worker_dashboard, name='worker_dashboard'),
    
    # Rasmlar
    path('upload-photo/', views.upload_work_photo, name='upload_work_photo'),
    
    # Buyurtmalar
    path('order/<int:worker_id>/', views.create_order, name='create_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Ishchilar
    path('workers/', views.worker_list, name='worker_list'),
    path('workers/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    
    # Sharhlar
    path('review/<int:worker_id>/', views.leave_review, name='leave_review'),
]




