from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import CustomUser
# إعادة توجيهه إلى الصفحة الرئيسية
    


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = request.POST.get("user_type")

        if password1 != password2:
            messages.error(request, "كلمات المرور غير متطابقة ⚠️")
            return render(request, "signup.html")

        # إنشاء المستخدم
        user = CustomUser.objects.create(
            username=username,
            email=email,
            user_type=user_type,
            password=make_password(password1)
        )

        # لو بائع نضيف بيانات المتجر
        if user_type == "vendor":
            business_name = request.POST.get("business_name")
            vendor_type = request.POST.get("vendor_type")
            logo = request.FILES.get("Logo")

            Vendor.objects.create(
                user=user,
                business_name=business_name,
                vendor_type=vendor_type,
                logo=logo
            )

        # تسجيل الدخول تلقائياً
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)

            # توجيه حسب نوع المستخدم
            if user.user_type == "vendor":
                return redirect("Vendor:vendor_dashboard")
            else:  # زبون عادي
                return redirect("Vendor:vendor")  # غيرها لأي صفحة تعرض المتاجر/المنتجات

        messages.error(request, "حدث خطأ أثناء تسجيل الدخول.")
        return redirect("login")  # fallback

    return render(request, "signup.html")



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'cart_detail')  # يرجع المستخدم للصفحة المطلوبة أو لسلة المشتريات
            return redirect(next_url)
        else:
            messages.error(request, 'اسم المستخدم أو كلمة السر غير صحيحة')
    return render(request, 'login.html')
