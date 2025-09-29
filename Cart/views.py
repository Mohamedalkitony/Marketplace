from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from Vendor.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart
from Order.models import Order, OrderItem
from decimal import Decimal
# Create your views here.


@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id = product_id)

    quantity = request.POST.get("quantity")
    override = request.POST.get("override")
    
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    override = True if override in ['True', 'true', '1'] else False

    cart.add_product(product=product,quantity=quantity,overrider_quantity=override)
    return redirect('Cart:cart_detail')
    

@require_POST
def cart_remov(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id = product_id)
    cart.Remove(product)
    return redirect('cart:cart_detial')


def cart_detial(request):
    cart = Cart(request)
    context = {
        'cart':cart
    }
    return render(request,'cart/cart_detail.html',context)

'''
#@login_required(login_url='/account/user_login/')
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart:cart_detail')

    # إزالة أي منتجات محذوفة من DB
    items_to_remove = []
    for item in cart:
        product = item.get('product')
        if product is None:
            items_to_remove.append(str(item.get('product_id')))

    for pid in items_to_remove:
        if pid in cart.cart:
            del cart.cart[pid]

    cart.save()  # حفظ التغييرات في session

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal(cart.total_price()),  # هنا ممكن تبقي Decimal في DB
            status='قيد الانتظار'
        )

        for item in cart:
            product = item.get('product')
            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(item['price']),  # تحويل السعر إلى Decimal قبل الحفظ في DB
                )

        cart.clear()  # إفراغ السلة بعد الطلب
        return redirect('Order:my_orders')

    context = {
        'cart': cart,
        'total': str(cart.total_price())
    }
    return render(request, 'cart/checkout.html', context)
'''



@login_required(login_url='/account/user_login/')
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart:cart_detail')

    # --- بداية التعديل ---

    # الخطوة 1: تحقق من المنتجات الموجودة بالفعل في قاعدة البيانات
    # هذا الجزء اختياري ولكنه ممارسة جيدة
    product_ids_in_cart = list(cart.cart.keys())
    existing_products = Product.objects.filter(id__in=product_ids_in_cart).values_list('id', flat=True)
    
    ids_to_remove = [pid for pid in product_ids_in_cart if int(pid) not in existing_products]

    if ids_to_remove:
        for product_id in ids_to_remove:
            # استخدم دالة الحذف من كلاس Cart إذا كانت موجودة
            # أو احذف مباشرة من القاموس
            if product_id in cart.cart:
                del cart.cart[product_id]
        cart.save() # احفظ فقط إذا قمت بالحذف

    # --- نهاية التعديل ---

    if request.method == 'POST':
        # لا حاجة للمرور على السلة مرة أخرى هنا، يمكنك استخدام البيانات مباشرة
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price(), # استخدم الدالة مباشرة
            status='قيد الانتظار'
        )

        # للحصول على المنتجات، قم بالمرور على السلة مرة أخرى
        for item in cart: # __iter__ ستعمل هنا وتجلب المنتجات
            OrderItem.objects.create(
                order=order,
                product=item['product'], # الآن 'product' موجود بفضل __iter__
                quantity=item['quantity'],
                price=Decimal(item['price']),
            )

        cart.clear()
        return redirect('Order:my_orders')

    # لا حاجة لتمرير 'total' بشكل منفصل، يمكن الوصول إليه من 'cart' في الـ template
    context = {
        'cart': cart,
    }
    return render(request, 'cart/checkout.html', context)