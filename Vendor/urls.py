

from django.contrib import admin
from django.urls import path
from .views import vendor_list,vendor_dashboard,add_product_view,edit_product_view,delete_product_view,vendor_products,product_detile,add_review,vendor_review
app_name ='Vendor'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vendor_list,name='vendor'),
    path('vendor_dashboard/',vendor_dashboard,name='vendor_dashboard'),
    path('add_product_view/',add_product_view,name='add_product_view'),
    path('edit_product_view/<int:pk>',edit_product_view,name='edit_product_view'),
    path('delete_product_view/<int:product_pk>/',delete_product_view,name='delete_product_view'),
    path('vendor_products/<int:vendor_id>',vendor_products,name='vendor_products'),
    path('product_detile/<int:product_id>/',product_detile, name='product_detile'),
    path('add_review/<int:vendor_id>/',add_review,name='add_review'),
    path('vendor_review<int:vendor_id>',vendor_review,name='vendor_review'),
]
