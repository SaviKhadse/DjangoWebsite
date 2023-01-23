from django.shortcuts import render, redirect
from .models import Customer, CustomerShippingAddress, Cart, CartItem
from vendor.models import Vendor
from product.models import Product, Category
from order.models import Order, OrderItem, OrderStatus
from common.models import Country, City, State
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib import messages
import decimal
# TemplateView.
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .dist import request_distance
import json
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
# For updating cart quantity if product already exists.
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count

# Create your views here.


# GET Cart Data.
def get_cart_details(request):
    current_user = request.user  # GET CURRENT USER.
    customer_id = int(Customer.objects.only('id').get(user=current_user.id).id)
    cart_id = int(Cart.objects.only('id').get(customer_id=customer_id).id)
    cart_items = CartItem.objects.prefetch_related(
        'product').filter(cart_id=cart_id)

    cart_total = 0
    for items in cart_items:
        cart_total += (items.quantity * items.product.price)

    cart_delievry_charges = decimal.Decimal(0.05) * cart_total

    return cart_items, cart_total, cart_delievry_charges


# GET Current User and Customer Data.
def get_current_user_and_customer_data(request):
    current_user = request.user  # GET CURRENT USER.
    customers = Customer.objects.get(user=current_user.id)
    users = User.objects.get(id=current_user.id)
    return customers, users


# CUSTOMER Registration View
def customer_registration(request):
    all_country = Country.objects.all()
    all_state = State.objects.all()
    all_city = City.objects.all()

    products = Product.objects.all()
    categories = Category.objects.all()

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

        # Code for Customer Model Save.
        phone_no = request.POST.get('phone_no')
        additional_phone_no = request.POST.get('additional_phone_no')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        country = int(request.POST.get('country'))
        state = int(request.POST.get('state'))
        city = int(request.POST.get('city'))
        zipcode = request.POST.get('zipcode')
        user_id = int(User.objects.only('id').get(username=username).id)

        if 'uploadedFromPC' in request.FILES:
            img = request.FILES['uploadedFromPC']
        else:
            img = ''

        customer_data = Customer(phone_no=phone_no,
                                 additional_phone_no=additional_phone_no, address_line1=address_line1, address_line2=address_line2,
                                 country_id=country, state_id=state, city_id=city, zipcode=zipcode, image=img, user_id=user_id)
        customer_data.save()
        customer_id = customer_data.id

        # Code to save shipping address.
        # Code for Customer Model Save.
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        country = int(request.POST.get('country'))
        state = int(request.POST.get('state'))
        city = int(request.POST.get('city'))
        zipcode = request.POST.get('zipcode')
        user_id = int(User.objects.only('id').get(username=username).id)

        customer_shipping_data = CustomerShippingAddress(address_line1=address_line1, address_line2=address_line2,
                                                         country_id=country, state_id=state, city_id=city, zipcode=zipcode, customer_id=customer_id)
        customer_shipping_data.save()

        # Code to create cart on successfully registration of customer.
        user_id = int(User.objects.only('id').get(username=username).id)
        customer_id = int(Customer.objects.only('id').get(user_id=user_id).id)
        customer_cart = Cart(customer_id=customer_id)
        customer_cart.save()

        return redirect('/customers/login/')

    return render(request, 'customer_html/customer_register.html', {'country': all_country, 'state': all_state, 'city': all_city, 'products': products, 'categories': categories})


# CUSTOMER Profile Edit View
def customer_profile_edit(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()

    # Get Cart Details.
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)

    current_user = request.user  # GET CURRENT USER.
    users = User.objects.get(id=current_user.id)
    customers = Customer.objects.get(user=current_user.id)
    return render(request, 'customer_html/customer_profile_edit.html', {
        'users': users,
        'customers': customers,
        'country': country,
        'state': state,
        'city': city
    })


# CUSTOMER Login View
class CustomerLoginView(LoginView):
    template_name = 'customer_html/index.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return '/customers/home/'


@login_required
def customer_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


# CUSTOMER home - Before Login
def home_before_login_view(request):
    # return HttpResponse('Hello! This is my first PROJECT')
    # return render(request, './home.html')  # Two buttons - Register and Login
    products = Product.objects.all()[:10]
    categories = Category.objects.all()

    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()

    return render(request, 'customer_html/index.html', {'products': products, 'categories': categories, 'country': country, 'state': state, 'city': city})


# CUSTOMER Home Page - After LOGIN (Logged View)
def customer_home(request):
    current_user = request.user  # GET CURRENT USER.
    print(current_user.id)
    if current_user.id is None:
        return redirect('/')
    else:
        users = User.objects.get(id=current_user.id)
        # customers = Customer.objects.get(user=current_user.id)
        customers = Customer.objects.get(user_id=current_user.id)
        print("Test = ", customers.image)

        # get cart details.
        cart_items, cart_total, cart_delivery_charges = get_cart_details(
            request)

        return render(request, 'customer_html/customer_homepage.html', {'users': users, 'customers': customers, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'cart_delivery_charges': round(cart_delivery_charges, 2)})


# CUSTOMER Product-Categories View
def product_category(request):
    # get cart details.
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)
    # get current user and customer data.
    customers, users = get_current_user_and_customer_data(request)

    category = Category.objects.all()
    return render(request, 'customer_html/product_category.html', {'category': category, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'customers': customers, 'users': users, 'cart_delivery_charges': round(cart_delivery_charges, 2)})


# CUSTOMER Category wise Products View
def category_wise_products(request, category_id):
    # cart_items, cart_total, cart_delivery_charges = get_cart_details(request) #get cart details.
    # customers, users = get_current_user_and_customer_data(request)   #get current user and customer data.

    # product = Product.objects.select_related('vendor').filter(category_id=category_id)
    # return render(request, 'customer_html/products.html', {'product': product, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'customers': customers, 'users': users, 'cart_delivery_charges': round(cart_delivery_charges, 2)})

    # get cart details.
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)
    # get current user and customer data.
    customers, users = get_current_user_and_customer_data(request)

    current_user = request.user  # GET CURRENT USER.
    customers = Customer.objects.prefetch_related(
        'city').get(user=current_user.id)
    customer_address = customers.address_line1 + ", " + \
        customers.city.city_name + " " + customers.zipcode

    vendor_distance = {}
    vendors = Vendor.objects.prefetch_related('city').all()
    for vendor in vendors:
        vendor_distance[vendor.id] = {
            'address': vendor.address_line1 + ", " + vendor.city.city_name + " " + vendor.zipcode
        }

    temp_product = []
    products = Product.objects.prefetch_related(
        'vendor').filter(category_id=category_id)[:80]
    print("type of object = ", type(products))
    for product in products:
        temp_product.append(
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'vendor': product.vendor.company_name,
                'image': product.image,
                'distance': calculate_distance(
                    origin=customer_address,
                    destination=vendor_distance[product.vendor.id]['address']
                )
            }
        )

    return render(request, 'customer_html/products.html', {'product': temp_product, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'customers': customers, 'users': users, 'cart_delivery_charges': round(cart_delivery_charges, 2)})


# CALCULATE Distance.
def calculate_distance(origin, destination):
    temp = request_distance(
        origin=origin,
        destination=destination
    )

    json_object = json.loads(temp)
    return json_object['rows'][0]['elements'][0]['distance']['text']


# CUSTOMER Product View
def products(request):
    # get cart details.
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)
    # get current user and customer data.
    customers, users = get_current_user_and_customer_data(request)

    current_user = request.user  # GET CURRENT USER.
    customers = Customer.objects.prefetch_related(
        'city').get(user=current_user.id)
    customer_address = customers.address_line1 + ", " + \
        customers.city.city_name + " " + customers.zipcode

    vendor_distance = {}
    vendors = Vendor.objects.prefetch_related('city').all()
    for vendor in vendors:
        vendor_distance[vendor.id] = {
            'address': vendor.address_line1 + ", " + vendor.city.city_name + " " + vendor.zipcode
        }

    temp_product = []
    products = Product.objects.prefetch_related('vendor').all()[:80]
    print("type of object = ", type(products))
    for product in products:
        temp_product.append(
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'vendor': product.vendor.company_name,
                'image': product.image,
                'distance': calculate_distance(
                    origin=customer_address,
                    destination=vendor_distance[product.vendor.id]['address']
                )
            }
        )

    return render(request, 'customer_html/products.html', {'product': temp_product, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'customers': customers, 'users': users, 'cart_delivery_charges': round(cart_delivery_charges, 2)})


def get_current_user_cart(request):
    current_user = request.user  # GET CURRENT USER.
    customer_id = int(Customer.objects.only('id').get(user=current_user.id).id)
    cart_id = int(Cart.objects.only('id').get(customer_id=customer_id).id)
    return cart_id


def add_to_cart(request):
    if request.method == "POST":
        # Code for CartItem Model Save.
        current_user = request.user  # GET CURRENT USER.
        customer_id = int(Customer.objects.only(
            'id').get(user=current_user.id).id)
        cart_id = int(Cart.objects.only('id').get(customer_id=customer_id).id)
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product')

        if CartItem.objects.filter(cart_id=cart_id, product_id=product_id).exists():
            CartItem.objects.filter(cart_id=cart_id, product_id=product_id).update(
                quantity=F('quantity')+1)
        else:
            cart_item = CartItem(
                cart_id=cart_id, product_id=product_id, quantity=quantity)
            cart_item.save()
        # messages.success(request, 'Your profile is updated successfully!')
        # return redirect('/customers/home/products')

    return HttpResponseRedirect(request.path_info)
    # return redirect('/customers/home/products')


def delete_from_cart(request, product_id):
    cart_id = get_current_user_cart(request)
    cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
    cart_item.delete()
    return redirect('/customers/home/products')


def remove_cart_items_after_placed_order(request):
    current_user = request.user  # GET CURRENT USER.
    customer_id = int(Customer.objects.only('id').get(user=current_user.id).id)
    cart_id = int(Cart.objects.only('id').get(customer_id=customer_id).id)
    cart_items = CartItem.objects.prefetch_related(
        'product').filter(cart_id=cart_id)
    cart_items.delete()
    return 'successfully remobed!'


def customer_create_order(request):
    customers, users = get_current_user_and_customer_data(request)
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)

    shipping_address = int(CustomerShippingAddress.objects.only(
        'id').get(customer_id=customers.id).id)
    order_status = int(OrderStatus.objects.only(
        'id').get(name='order_placed').id)

    # Save Order Model Data.
    # create_order = Order(customer_id=customers.id, shipping_address=shipping_address, order_status_id=order_status)
    # create_order.save()
    # order_id = create_order.id

    try:
        vendors = []
        vendor_order = {}
        for cart_item in cart_items:
            print(cart_item.product.vendor_id)
            if (cart_item.product.vendor_id not in vendors):
                print("in loop now")
                # Save Order data.
                create_order = Order(
                    customer_id=customers.id,
                    shipping_address_id=shipping_address,
                    order_status_id=order_status,
                    vendor_id=cart_item.product.vendor_id,
                    delivery_charges=decimal.Decimal(5.00)
                )
                create_order.save()

                print("Order created")
                order_id = create_order.id
                vendors.append(cart_item.product.vendor_id)
                vendor_order[cart_item.product.vendor_id] = order_id
                print(vendor_order)
                # Save Order Item data.
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    order_status_id=order_status
                )
                order_item.save()

            else:
                print("In else part")
                # Save Order Item data.
                order_item = OrderItem(
                    order_id=vendor_order[cart_item.product.vendor_id],
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    order_status_id=order_status
                )
                order_item.save()

        temp = {
            'success': 1
        }

        # Remove cart items after order placed successfully.
        remove_cart_items_after_placed_order(request)

        # Return homepage.
        current_user = request.user  # GET CURRENT USER.
        if current_user.id is None:
            return redirect('/')
        else:
            users = User.objects.get(id=current_user.id)
            # customers = Customer.objects.get(user=current_user.id)
            customers = Customer.objects.get(user_id=current_user.id)
            print("Test = ", customers.image)

            # get cart details.
            cart_items, cart_total, cart_delivery_charges = get_cart_details(
                request)

            return render(request, 'customer_html/customer_homepage.html', {'users': users, 'customers': customers, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'cart_delivery_charges': round(cart_delivery_charges, 2), 'message': temp})

    except:
        temp = {
            'error': 1
        }
        print("got error")
        messages.error(
            request, "Something went wrong! Order didn't placed. Please try after sometime.")
        return HttpResponseRedirect('/customers/home/')


def customer_display_order(request):
    customers, users = get_current_user_and_customer_data(request)
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)
    orders = Order.objects.select_related('vendor', 'order_status').filter(
        customer_id=customers.id).annotate(no_of_items=Count('orderitem__order'))
    print(orders)
    return render(request, 'customer_html/customer_orders.html', {'users': users, 'customers': customers, 'cart_items': cart_items, 'cart_total': round(cart_total, 2), 'cart_delivery_charges': round(cart_delivery_charges, 2), 'orders': orders})


def customer_display_order_details(request, order_id):
    customers, users = get_current_user_and_customer_data(request)
    cart_items, cart_total, cart_delivery_charges = get_cart_details(request)

    order_details = OrderItem.objects.select_related(
        'product', 'product__vendor').filter(order_id=order_id)
    order_total = 0
    estimated_tax = 0
    for order_item in order_details:
        order_total += (order_item.price * order_item.quantity)
        estimated_tax += (order_item.price * order_item.quantity) * \
            (order_item.product.estimated_tax/100)

    shipping_charges = order_total * decimal.Decimal(0.05)
    final_total = order_total + estimated_tax + shipping_charges

    return render(request, 'customer_html/customer_order_details.html', {
        'users': users,
        'customers': customers,
        'cart_items': cart_items,
        'cart_total': round(cart_total, 2),
        'cart_delivery_charges': round(cart_delivery_charges, 2),
        'order_details': order_details,
        'order_total': round(order_total, 2),
        'estimated_tax': round(estimated_tax, 2),
        'shipping_charges': round(shipping_charges, 2),
        'final_total': round(final_total, 2)
    })
