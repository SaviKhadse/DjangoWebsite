from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomerLoginView
from rest_framework.routers import SimpleRouter
# from rest_framework_nested import routers
from django.conf import settings
from django.conf.urls.static import static

# router = SimpleRouter()
# router.register('', views.customer_register, basename='customers')
# router.register('', views.CustomerViewSet, basename='customers')


# # urlpatterns = [
# # 	path('', views.home_view, name='home_view'),
# # 	path('register', views.register_view, name='register_view'),
# # 	path('form', views.my_form, name='my_form'),
# # 	path('login', views.login_view, name='login_view'),
# # ]

# urlpatterns = router.urls


urlpatterns = [
    path('', views.home_before_login_view, name='home_view'),
    path('register/', views.customer_registration, name='customer_register'),
    path('login/', CustomerLoginView.as_view(), name='customer_login'),
    path('logout/', views.customer_logout, name='logout'),
	path('home/', views.customer_home, name='customer_home'),
    path('home/categories', views.product_category, name='product_category'),
    path('home/products', views.products, name='products'),
    path('home/categories/<category_id>/products/', views.category_wise_products, name='category_wise_products'),
    path('home/customer_profile_edit/', views.customer_profile_edit, name='customer_profile_edit'),
	path('home/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('home/cart/product/remove/<product_id>', views.delete_from_cart, name='category_wise_products'),
	path('home/orders/', views.customer_display_order, name='customer_display_order'),
	path('home/orders/<order_id>', views.customer_display_order_details, name='customer_display_order_details'),
	path('home/orders/create_order/', views.customer_create_order, name='customer_create_order'),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)