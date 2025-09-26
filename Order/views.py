from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order


@login_required
def vendor_orders(request):
    # افترض أن التاجر مربوط بـ user.vendor
    orders = Order.objects.filter(items__product__vendor=request.user.vendor).distinct()
    return render(request, 'Order/vendor_orders.html', {'orders': orders})



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Order/my_orders.html', {'orders': orders})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'Order/order_detail.html', {'order': order})
