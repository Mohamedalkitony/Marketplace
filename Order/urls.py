from django.urls import path
from .views import my_orders,vendor_orders,order_detail
app_name ='Order'
urlpatterns = [
    path('vendor_orders/',vendor_orders,name='vendor_orders'),
    path('my_orders/',my_orders,name='my_orders'),
    path('order_detail/<int:order_id>',order_detail,name='order_detail'),
]