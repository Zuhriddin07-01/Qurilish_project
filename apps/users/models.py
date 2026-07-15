from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT  = 'client',  'Mijoz'
        BUILDER = 'builder', 'Quruvchi'
        ADMIN   = 'admin',   'Admin'

    role       = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone      = models.CharField(max_length=20, blank=True)
    avatar     = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address    = models.CharField(max_length=255, blank=True)
    bio        = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
