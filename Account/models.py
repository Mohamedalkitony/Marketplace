from django.db import models
from django.contrib.auth.models import AbstractUser # نستخدم AbstractUser لإنشاء نموذج مستخدم مخصص

# نموذج المستخدم المخصص (Custom User Model)
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')

# نموذج البائع (Vendor)
class Vendor(models.Model):
    VENDOR_TYPES = (
        ('gym', 'Gym'),
        ('trainer', 'Personal Trainer'),
        ('sportswear', 'Sportswear Shop'),
        ('supplements', 'Supplement Store'),
        ('equipment', 'Fitness Equipment Vendor'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPES)
    logo = models.ImageField(upload_to='media', default='default.png')
    
    # حقل تحديد حالة النشاط
    is_active = models.BooleanField(default=True)
    
    # خيارات الاشتراك
    is_subscription_active = models.BooleanField(default=False)
    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # خيار العمولة
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.business_name
