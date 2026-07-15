from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import Worker, Order, WorkPhoto, WorkerReview

@login_required
def create_worker_profile(request):
    # Agar foydalanuvchi allaqachon ishchi profilega ega bo'lsa
    if hasattr(request.user, 'worker_profile'):
        messages.warning(request, "Siz allaqachon ishchi profilingizni yaratgansiz!")
        return redirect('worker_dashboard')
    
    if request.method == 'POST':
        # Ma'lumotlarni olish
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        profession = request.POST.get('profession')
        experience = request.POST.get('experience', 0)
        bio = request.POST.get('bio', '')
        
        # Validatsiya
        if not full_name or not phone or not profession:
            messages.error(request, "Barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'common/create_worker_profile.html')
        
        # Yangi ishchi profile yaratish
        worker = Worker.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            profession=profession,
            experience=int(experience) if experience else 0,
            bio=bio,
            is_available=True
        )
        
        messages.success(request, f"Hurmatli {worker.full_name}, profilingiz muvaffaqiyatli yaratildi!")
        return redirect('worker_dashboard')
    
    return render(request, 'common/create_worker_profile.html')


@login_required
def worker_dashboard(request):
    # Ishchining dashboardi
    try:
        worker = request.user.worker_profile
        orders = Order.objects.filter(worker=worker).order_by('-created_at')
        photos = WorkPhoto.objects.filter(worker=worker).order_by('-created_at')
        reviews = WorkerReview.objects.filter(worker=worker).order_by('-created_at')
        
        context = {
            'worker': worker,
            'orders': orders,
            'photos': photos,
            'reviews': reviews,
            'orders_count': orders.count(),
            'photos_count': photos.count(),
            'reviews_count': reviews.count(),
            'average_rating': worker.rating,
        }
        return render(request, 'common/worker_dashboard.html', context)
    except:
        messages.warning(request, "Iltimos, avval profilingizni yarating!")
        return redirect('create_worker_profile')


@login_required
def upload_work_photo(request):
    # Ishchi o'z ishini suratga olib yuklaydi
    if not hasattr(request.user, 'worker_profile'):
        messages.error(request, "Avval ishchi profilingizni yarating!")
        return redirect('create_worker_profile')
    
    worker = request.user.worker_profile
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        
        if not title or not image:
            messages.error(request, "Rasm va nom majburiy!")
            return render(request, 'common/upload_photo.html')
        
        photo = WorkPhoto.objects.create(
            worker=worker,
            title=title,
            description=description,
            location=location,
            image=image
        )
        
        messages.success(request, "Rasm muvaffaqiyatli yuklandi!")
        return redirect('worker_dashboard')
    
    return render(request, 'common/upload_photo.html')


@login_required
def create_order(request, worker_id):
    # Mijoz ishchiga buyurtma beradi
    worker = get_object_or_404(Worker, id=worker_id, is_available=True)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')
        address = request.POST.get('address')
        description = request.POST.get('description')
        scheduled_date = request.POST.get('scheduled_date')
        
        # Validatsiya
        if not customer_name or not customer_phone or not address:
            messages.error(request, "Barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'common/create_order.html', {'worker': worker})
        
        order = Order.objects.create(
            worker=worker,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            address=address,
            description=description,
            scheduled_date=scheduled_date if scheduled_date else None,
            status='pending'
        )
        
        messages.success(request, f"Buyurtmangiz qabul qilindi! {worker.full_name} bilan bog'lanamiz.")
        return redirect('order_success', order_id=order.id)
    
    return render(request, 'common/create_order.html', {'worker': worker})


@login_required
def order_success(request, order_id):
    # Buyurtma muvaffaqiyatli yaratilgan sahifa
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'common/order_success.html', {'order': order})


@login_required
def worker_list(request):
    # Barcha ishchilar ro'yxati
    workers = Worker.objects.filter(is_available=True).order_by('-rating')
    
    # Qidiruv
    query = request.GET.get('q')
    if query:
        workers = workers.filter(
            models.Q(full_name__icontains=query) |
            models.Q(profession__icontains=query)
        )
    
    context = {
        'workers': workers,
        'query': query,
    }
    return render(request, 'common/worker_list.html', context)


@login_required
def worker_detail(request, worker_id):
    # Ishchi haqida batafsil ma'lumot
    worker = get_object_or_404(Worker, id=worker_id)
    photos = WorkPhoto.objects.filter(worker=worker).order_by('-created_at')[:10]
    reviews = WorkerReview.objects.filter(worker=worker).order_by('-created_at')[:5]
    
    context = {
        'worker': worker,
        'photos': photos,
        'reviews': reviews,
    }
    return render(request, 'common/worker_detail.html', context)


@login_required
def leave_review(request, worker_id):
    # Mijoz ishchini baholaydi
    worker = get_object_or_404(Worker, id=worker_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        customer_name = request.POST.get('customer_name')
        
        if rating < 1 or rating > 5:
            messages.error(request, "Baholash 1 dan 5 gacha bo'lishi kerak!")
            return render(request, 'common/leave_review.html', {'worker': worker})
        
        review = WorkerReview.objects.create(
            worker=worker,
            customer_name=customer_name,
            rating=rating,
            comment=comment
        )
        
        # Ishchining umumiy reytingini yangilash
        all_reviews = WorkerReview.objects.filter(worker=worker)
        average_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
        worker.rating = round(average_rating, 1)
        worker.save()
        
        messages.success(request, "Rahmat! Sizning fikringiz muhim.")
        return redirect('worker_detail', worker_id=worker.id)
    
    return render(request, 'common/leave_review.html', {'worker': worker})


@login_required
def my_orders(request):
    # Mijozning buyurtmalari
    orders = Order.objects.filter(customer_name=request.user.get_full_name()).order_by('-created_at')
    return render(request, 'common/my_orders.html', {'orders': orders})

