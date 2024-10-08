from django.urls import path
from ProjectWebGame import views

app_name = "ProjectWebGame"

urlpatterns = [
    path('',views.index,name='index'),
    path('contact',views.contact,name='contact'),
    path('productDetails',views.productDetails,name='productDetails'),
    path('shop',views.shop,name='shop'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
]