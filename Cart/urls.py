from django.urls import path
from .views import cart_add,cart_detial,checkout
app_name ='Cart'
urlpatterns = [
    path('cart_add/<int:product_id>/',cart_add,name='cart_add'),
    path('cart_detail',cart_detial,name='cart_detail'),
    path('checkout/',checkout,name='checkout'),
]