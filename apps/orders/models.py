from django.db import models
from django.conf import settings


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Kutilmoqda'
        ACCEPTED  = 'accepted',  'Qabul qilindi'
        IN_WORK   = 'in_work',   'Bajarilmoqda'
        DONE      = 'done',      'Tugallandi'
        CANCELLED = 'cancelled', 'Bekor qilindi'
        REJECTED  = 'rejected',  'Rad etildi'

    client      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    title       = models.CharField(max_length=255)
    description = models.TextField()
    address     = models.CharField(max_length=255)
    budget      = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status      = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Zakaz #{self.pk} — {self.client}"

    class Meta:
        ordering = ['-created_at']
