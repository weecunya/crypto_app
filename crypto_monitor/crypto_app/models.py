
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserInfo(AbstractUser):
    email = models.EmailField(unique=True,default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class CryptoPrice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length = 10)
    price = models.DecimalField(max_digits=20, decimal_places=8)

    class Meta:
        indexes = [
            models.Index(fields=['symbol','-timestamp'])
        ]
        def __str__(self):
            return f"{self.symbol}: {self.price} at {self.timestamp}"