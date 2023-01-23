from django.contrib import admin
from . import models

# Register your models here.
# @admin.register(models.Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'full_name', 'email', 'phone_no', 'address_line1','address_line2','city','state','zipcode']
#     ordering = ['first_name', 'last_name']
#     search_fields = ['first_name__istartswith', 'last_name__istartswith']

#     def full_name(self, customer):
#         return customer.first_name + ' ' + customer.last_name


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'address_line1','address_line2','city','state','zipcode']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.CustomerShippingAddress)
class CustomerShippingAddressAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer', 'city', 'state', 'country']
    list_display = ['id','customer', 'address_line1','address_line2','city','state','zipcode']
    search_fields = ['customer']

class CartItemInline(admin.TabularInline):
    model = models.CartItem
    autocomplete_fields = ['product']
    extra = 2

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'added_on', 'modified_on']
    autocomplete_fields = ['customer']
    inlines = [CartItemInline]

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'price', 'added_on', 'modified_on']
    ordering = ['id']
    search_fields = ['cart__customer__first_name__istartswith', 'cart__customer__last_name__istartswith']
    def price(self, cartitem):
        return cartitem.product.price