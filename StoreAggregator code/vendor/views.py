from django.shortcuts import render, redirect
from common.models import Country, City, State
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Vendor
from product.models import Product, Category
from order.models import OrderItem, Order, OrderStatus
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework.decorators import api_view
from django.contrib.auth.views import LoginView
import decimal
from django.core.exceptions import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def get_current_user(request):
    current_user = request.user  # GET CURRENT USER.
    vendor_id = int(Vendor.objects.only('id').get(user=current_user.id).id)
    return vendor_id


def get_current_user_and_vendor_data(request):
    current_user = request.user  # GET CURRENT USER.
    vendors = Vendor.objects.get(user=current_user.id)
    users = User.objects.get(id=current_user.id)
    return vendors, users

# VENDOR Registration


def vendor_register(request):
    all_country = Country.objects.all()
    all_state = State.objects.all()
    all_city = City.objects.all()

    if request.method == "POST":
        # Code for User Model Save.
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))

        user_data = User(first_name=first_name, last_name=last_name,
                         email=email, username=username, password=password)
        user_data.save()

        # Code for Vendor Model Save.
        company_name = request.POST.get('company_name')
        license_no = request.POST.get('license_no')
        phone_no = request.POST.get('phone_no')
        alternate_contact = request.POST.get('alternate_contact')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        country = int(request.POST.get('country'))
        state = int(request.POST.get('state'))
        city = int(request.POST.get('city'))
        zipcode = request.POST.get('zipcode')
        website = request.POST.get('website')
        user_id = int(User.objects.only('id').get(username=username).id)

        vendor_data = Vendor(
            company_name=company_name,
            license_no=license_no,
            phone_no=phone_no,
            alternate_contact=alternate_contact,
            address_line1=address_line1,
            address_line2=address_line2,
            country_id=country,
            state_id=state,
            city_id=city,
            zipcode=zipcode,
            website=website,
            user_id=user_id
        )

        vendor_data.save()
        return render(request, 'vendor_html/vendor_login.html', {'country': all_country, 'state': all_state, 'city': all_city})
        # return render(request, 'vendor_html/user-add.html', {'country': all_country, 'state':all_state, 'city':all_city})

    return render(request, 'vendor_html/vendor_register.html', {'country': all_country, 'state': all_state, 'city': all_city})


# VENDOR Login
class VendorLoginView(LoginView):
    template_name = 'vendor_html/vendor_login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return '/vendors/home/'


# VENDOR Logout
@login_required
def vendor_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/vendors/login/')


# VENDOR Home
def vendor_home(request):
    order_status = OrderStatus.objects.all()
    current_user = request.user
    print("USER DATA = ", current_user.id)
    if current_user.id is None:
        return redirect('/')
    else:
        users = User.objects.get(id=current_user.id)
        vendors = Vendor.objects.get(user_id=current_user.id)
        print(vendors)
        print(users)
        return render(request, 'vendor_html/vendor_homepage.html', {'vendors': vendors, 'users': users, 'order_status': order_status})


# VENDOR Dashboard
def vendor_dashborad(request):
    vendors, users = get_current_user_and_vendor_data(request)
    return render(request, 'vendor_html/vendor_dashboard.html', {'vendors': vendors, 'users': users})


# VENDOR Product-List
def main_category_wise_products(request, store_category):
    vendors, users = get_current_user_and_vendor_data(request)
    products = Product.objects.filter(
        store_category=store_category, vendor_id=vendors.id)
    return render(request, 'vendor_html/vendor_list_product.html', {'products': products, 'vendors': vendors, 'users': users})


# VENDOR Add Product.
def vendor_add_product(request):
    vendors, users = get_current_user_and_vendor_data(request)
    categories = Category.objects.all()
    if request.method == "POST":
        # Code for User Model Save.
        name = request.POST.get('name')
        description = request.POST.get('description')
        store_category = request.POST.get('store_category')
        category = int(request.POST.get('category'))
        estimated_tax = decimal.Decimal(request.POST.get('estimated_tax'))
        price = decimal.Decimal(request.POST.get('price'))
        inventory = decimal.Decimal(request.POST.get('inventory'))
        if request.POST.get('weight'):
            weight = decimal.Decimal(request.POST.get('weight'))
        else:
            weight = 0

        if request.POST.get('size'):
            size = decimal.Decimal(request.POST.get('size'))
        else:
            size = 0

        if 'uploadedFromPC' in request.FILES:
            img = request.FILES['uploadedFromPC']
        else:
            img = ''
        vendor = get_current_user(request)

        product_data = Product(
            name=name,
            description=description,
            store_category=store_category,
            category_id=category,
            estimated_tax=estimated_tax,
            price=price,
            inventory=inventory,
            weight=weight,
            size=size,
            image=img,
            vendor_id=vendor,
        )

        try:
            product_data.save()
            temp = {
                'success': 1
            }
            return render(request, 'vendor_html/vendor_add_product.html', {'categories': categories, 'messages': temp, 'vendors': vendors, 'users': users})
        except:
            temp = {
                'error': 1
            }
            return render(request, 'vendor_html/vendor_add_product.html', {'categories': categories, 'messages': temp, 'vendors': vendors, 'users': users})

    return render(request, 'vendor_html/vendor_add_product.html', {'categories': categories, 'vendors': vendors, 'users': users})


def my_orders(request):
    vendors, users = get_current_user_and_vendor_data(request)
    order_status = OrderStatus.objects.all()

    orders = Order.objects.select_related('customer__user', 'order_status').filter(
        vendor_id=get_current_user(request)).order_by('id')
    order_items = OrderItem.objects.select_related(
        'order__customer__user',
        'product',
        'product__vendor').filter(order_id__in=orders).order_by('order_id')

    return render(request, 'vendor_html/my_orders.html', {
        'orders': orders,
        'order_items': order_items,
        'vendors': vendors,
        'users': users,
        'order_status': order_status
    })


def filter_my_orders(request, order_status_id):
    vendors, users = get_current_user_and_vendor_data(request)
    order_status = OrderStatus.objects.all()

    orders = Order.objects.select_related('customer__user', 'order_status').filter(
        order_status_id=order_status_id, vendor_id=get_current_user(request)).order_by('id')
    order_items = OrderItem.objects.select_related(
        'order__customer__user',
        'product',
        'product__vendor').filter(order_id__in=orders).order_by('order_id')

    return render(request, 'vendor_html/my_orders.html', {
        'orders': orders,
        'order_items': order_items,
        'vendors': vendors,
        'users': users,
        'order_status': order_status
    })


def change_order_status(request, order_id):
    Order.objects.filter(pk=order_id).update(order_status_id=int(
        OrderStatus.objects.only('id').get(name='ready_for_dispatch').id))
    OrderItem.objects.filter(order_id=order_id).update(order_status_id=int(
        OrderStatus.objects.only('id').get(name='ready_for_dispatch').id))

    return redirect('/vendors/home/orders/')
