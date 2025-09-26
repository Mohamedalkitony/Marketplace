from django.db import models
from Account.models import CustomUser
from Vendor.models import Product
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('قيد التوصيل', 'قيد التوصيل'),  # خيار جديد
        ('مكتمل', 'مكتمل'),
        ('ملغي', 'ملغى'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"طلب #{self.id} - {self.user.username}"
class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('delivery', 'قيد التوصيل'),  # خيار جديد
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')