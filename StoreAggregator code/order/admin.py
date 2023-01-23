from itertools import product
from django.contrib import admin

from product.models import Product
from . import models

# Register your models here.
@admin.register(models.OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'remark']
    search_fields = ['name']

#This class to display products in Order Model.
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['order', 'product']
    extra = 2
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'shipping_address', 'order_status', 'added_on']
    list_editable = ['order_status']
    autocomplete_fields = ['customer', 'shipping_address']
    search_fields = ['customer']
    ordering = ['id']
    inlines = [OrderItemInline]

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'order_status', 'added_on']
    autocomplete_fields = ['order', 'product']
    search_fields = ['order']
    ordering = ['id']

    def price(self, product):
        return product.price