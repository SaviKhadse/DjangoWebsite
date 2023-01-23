from rest_framework import serializers
from .models import Customer, CustomerShippingAddress
from common.models import Country, City, State

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_no', 'additional_phone_no', 'country', 'state', 'city', 'address_line1', 'address_line2', 'zipcode']
        # fields = '__all__'