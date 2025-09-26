# في ملف app_name/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser # نستخدم AbstractUser لإنشاء نموذج مستخدم مخصص
from Account.models import CustomUser,Vendor 
# باقي النماذج (Product, Review, Transaction) تبقى كما هي
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    PRODUCT_CATEGORIES = (
        ('sportswear', 'Sportswear'),
        ('supplements', 'Supplements'),
        ('equipment', 'Fitness Equipment'),
        ('membership', 'Gym Membership'),
        ('training', 'Personal Training Session'),
    )
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORIES)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.vendor.business_name}'

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f'Transaction {self.id} - {self.status}'