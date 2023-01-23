from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import VendorLoginView
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('login/', VendorLoginView.as_view(), name='vendor_login'),
    path('logout/', views.vendor_logout, name='vendor_logout'),
    path('register/', views.vendor_register, name='vendor_register'),
    path('home/products/list-product/<store_category>', views.main_category_wise_products, name='main_category_wise_products'),
	path('home/', views.vendor_home, name='vendor_home'),
	path('dashboard/', views.vendor_dashborad, name='vendor_dashborad'),
	path('home/products/add_product/', views.vendor_add_product, name='vendor_add_product'),
	path('home/orders/', views.my_orders, name='my_orders'),
	path('home/orders/<order_status_id>', views.filter_my_orders, name='filter_my_orders'),
	path('home/orders/change_status/<order_id>', views.change_order_status, name='change_order_status'),
]