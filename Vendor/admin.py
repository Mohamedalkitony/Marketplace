from django.contrib import admin
from .models import Vendor, Product
'''
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'vendor_type', 'is_active', 'is_subscription_active')
    list_filter = ('vendor_type', 'is_active', 'is_subscription_active')
    search_fields = ('business_name', 'user__email')  # تبحث بالاسم والايميل
    ordering = ('business_name',)
'''
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'category')
    list_filter = ('category', 'vendor')
    search_fields = ('name', 'description')
    ordering = ('-price',)
