from django import forms
from django.contrib.auth.models import User
from .models import Customer, CustomerDummy
from django.contrib.auth.models import User
from django.forms import *

class MyForm(ModelForm):
  class Meta:
    model = Customer
    fields = ["email", "first_name", "last_name", "password", "phone_no", "additional_phone_no", "country", "address_line1", "address_line2", "state", "city", "zipcode"]
    # labels = {'fullname': "Name", "mobile_number": "Mobile Number",}
    # widgets = {
    #         'first_name': TextInput(attrs={
    #             'class': "form-control",
    #             'style': 'max-width: 300px;',
    #             'placeholder': 'First--Name'
    #             }),
    #         'email': EmailInput(attrs={
    #             'class': "form-control", 
    #             'style': 'max-width: 300px;',
    #             'placeholder': 'Last Name'
    #             })
    #     }

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "email", "username", "password"]

class CustomerDummyForm(ModelForm):
  class Meta:
    model = CustomerDummy
    fields = ["phone_no", "additional_phone_no", "country", "address_line1", "address_line2", "state", "city", "zipcode"]