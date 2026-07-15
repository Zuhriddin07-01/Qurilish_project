from django.db import models
from django.conf import settings


class Worker(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.profession}"

    class Meta:
        ordering = ['-rating', 'full_name']


class WorkPhoto(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='work_photos/%Y/%m/%d/')
    description = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.worker.full_name} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('accepted', 'Qabul qilingan'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
    ]
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(null=True, blank=True)
    address = models.TextField(max_length=300)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateField(null=True, blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.worker.full_name if self.worker else 'Aniqlanmagan'}"

    class Meta:
        ordering = ['-created_at']


class WorkerReview(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.worker.full_name} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']

