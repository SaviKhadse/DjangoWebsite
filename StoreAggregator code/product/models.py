from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, null=False)
    remark = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    
    STORE_CATEGORY_MED = 'Medicine'
    STORE_CATEGORY_GRO = 'Grocery'
    STORE_CATEGORY = [
        (STORE_CATEGORY_MED, 'Medicine'),
        (STORE_CATEGORY_GRO, 'Grocery')
    ]
    
    name = models.CharField(max_length=60, null=False)
    description = models.TextField(null=True)
    store_category = models.CharField(
        max_length=10, choices=STORE_CATEGORY, default=STORE_CATEGORY_GRO
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    estimated_tax = models.DecimalField(max_digits=4, decimal_places=2, default=10.25)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    inventory = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    # image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    # image = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images')
    
    #Foreign Keys
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Products'