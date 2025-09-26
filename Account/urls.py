from django.contrib import admin
from django.urls import path
from .views import signup_view,user_login
from django.conf.urls.static import static
from Marcetplace2 import settings
app_name ='Account'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('/signup_view',signup_view,name='signup_view'),
    path('account/user_login/',user_login, name='user_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)