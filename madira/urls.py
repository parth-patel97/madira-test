"""madira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('eotp/',views.eotp,name='eotp'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('shop/',views.product,name='shop'),
    path('productdetail/',views.productdetail,name='productdetail'),
    path('addtocart/<int:id>/',views.addtocart,name='addtocart'),
    path('contact/',views.contact,name='contact'),
    path('category/',views.category,name='category'),
    path('showcart/',views.showcart,name='showcart'),
    path('plus/<int:id>/',views.plus,name='plus'),
    path('minus/<int:id>/',views.minus,name='minus'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('checkout/',views.checkout,name='checkout'),
    path('account/',views.myaccount,name='myaccount'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('about/',views.about,name='about'),
    path('OrderConform/',views.OrderConform,name='OrderConform'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
