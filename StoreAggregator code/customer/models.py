from email.headerregistry import UniqueAddressHeader
from email.policy import default
from enum import unique
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from common.models import City, State, Country

# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     phone_no = models.CharField(max_length=20)
#     additional_phone_no = models.CharField(max_length=20, null=True, blank=True)
#     country = models.ForeignKey(Country, on_delete=models.PROTECT)
#     address_line1 = models.CharField(max_length=50, null=False)
#     address_line2 = models.CharField(max_length=50, null=True, blank=True)
#     state = models.ForeignKey(State, on_delete=models.PROTECT)
#     city = models.ForeignKey(City, on_delete=models.PROTECT)
#     zipcode = models.CharField(max_length=10, null=False)
#     # user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return f'{self.first_name} {self.last_name}'

#     class Meta:
#         ordering = ['first_name', 'last_name']
#         verbose_name_plural = 'Customer'




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    phone_no = models.CharField(max_length=20)
    additional_phone_no = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address_line1 = models.CharField(max_length=50, null=False)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='customercities')
    zipcode = models.CharField(max_length=10, null=False)
    image = models.ImageField(upload_to='customer_images')


class CustomerShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50, null=False)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=False)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.address_line1}, {self.address_line2}, {self.city}, {self.state}-{self.zipcode}'

    class Meta:
        verbose_name_plural = 'Customer Shipping Address'

class Cart(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return f'{self.id} - {self.customer}'

    # class Meta:
    #     verbose_name_plural = 'Customer Cart'



# class CartItem(models.Model):
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    #Foreign Key
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return f'{self.cart}'
    
    # class Meta:
    #     verbose_name_plural = 'Cart Items'