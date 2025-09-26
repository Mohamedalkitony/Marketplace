from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vendor, Product
from django.contrib.auth.decorators import login_required
from .models import Vendor, Product,Review
from django.contrib import messages
from Order.models import Order
def vendor_list(request):
    """
    يعرض قائمة بجميع المتاجر النشطة على المنصة.
    """
    vendors = Vendor.objects.filter(is_active=True)
    return render(request, 'vendor_list.html', {'vendors': vendors})






@login_required
def vendor_dashboard(request):
    try:
        vendor = request.user.vendor
        if not vendor.is_active:
            # إذا كان البائع غير نشط، يمكن إظهار رسالة له
            return render(request, 'dashboard/pending_approval.html')

        products = Product.objects.filter(vendor=vendor)
        # يمكنك إضافة المزيد من البيانات مثل الإحصائيات والمبيعات
        context = {
            'vendor': vendor,
            'products': products,
        }
        return render(request, 'dashboard/vendor_dashboard.html', context)
    except Vendor.DoesNotExist:
        # إذا لم يكن المستخدم بائعًا
        return redirect('Vendor:vendor')  
    

    

@login_required
def add_product_view(request):
    try:
        vendor = request.user.vendor  # جرب نجيب vendor المرتبط بالمستخدم
    except Vendor.DoesNotExist:
        messages.error(request, "أنت مش مرتبط بأي متجر، ما تقدر تضيف منتجات.")
        return redirect('Vendor:vendor')  # أو أي صفحة مناسبة

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        # التحقق من أن البائع فعلاً نشط (اختياري)
        if not vendor.is_active:
            messages.error(request, "متجرك غير نشط، لا يمكنك إضافة منتجات.")
            return redirect('dashboard/vendor_dashboard')

        Product.objects.create(
            vendor=vendor,
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )

        messages.success(request, "تم إضافة المنتج بنجاح!")
        return redirect('Vendor:vendor_dashboard')

    return render(request, 'dashboard/add_product.html')


@login_required
def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user.vendor)
    categorys = Product.PRODUCT_CATEGORIES
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.category = request.POST.get("category")
        if request.FILES.get("image"):
            product.image = request.FILES.get("image")
        product.save()

        return redirect('Vendor:vendor')

    return render(request, "dashboard/edit_product.html", {"product": product,"categorys":categorys})


@login_required
def delete_product_view(request, product_pk):
    product = get_object_or_404(Product, id=product_pk)
    
    # تأكد إنو البائع صاحب المنتج فقط يقدر يحذفه
    if product.vendor != request.user.vendor:
        messages.error(request, "مش مسموحلك تحذف هذا المنتج.")
        return redirect('dashboard/vendor_dashboard')  # أو أي صفحة تحبها

    if request.method == "POST":
        product.delete()
        messages.success(request, "تم حذف المنتج بنجاح!")
        return redirect('Vendor:vendor_dashboard')
    


def vendor_products(request,vendor_id):
    vendor = get_object_or_404(Vendor,pk=vendor_id)
    if vendor.is_active:
        products = Product.objects.filter(vendor=vendor)
    return render(request,'vendor_products.html',{'products':products,'vendor':vendor}) 


def product_detile(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_detil.html', {'product': product})



@login_required
def add_review(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating:
            Review.objects.create(
                user=request.user,
                vendor=vendor,
                rating=rating,
                comment=comment
            )
        return redirect('Vendor:vendor_products', vendor_id=vendor.id)

    return redirect('Vendor:vendor_products', vendor_id=vendor.id)


@login_required
def vendor_review(request,vendor_id):
    
    vendor = get_object_or_404(Vendor,pk = vendor_id)
    reviews = Review.objects.filter(vendor=vendor)
    
    return render(request,'vendor_review.html',{'reviews':reviews})