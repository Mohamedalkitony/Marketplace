# Order/admin.py
from django.contrib import admin
from .models import Order, OrderItem

# Inline class لعرض عناصر الطلب داخل صفحة الطلب
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # عدد الأسطر الإضافية الفارغة
    readonly_fields = ('product', 'quantity', 'price')  # لمنع التعديل مباشرة إذا تحب

# صفحة Order في الـ admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')  # الأعمدة اللي تظهر في قائمة الطلبات
    list_filter = ('status', 'created_at')  # فلاتر على الجانب
    search_fields = ('user__username', 'id')  # البحث باليوزر أو رقم الطلب
    inlines = [OrderItemInline]  # ربط العناصر داخل صفحة الطلب
    readonly_fields = ('created_at', 'total_price')  # منع تعديل بعض الحقول

# لو تحب تقدر تضيف OrderItem منفصل في الـ admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('product',)
    search_fields = ('order__id', 'product__name')
