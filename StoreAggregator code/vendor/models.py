from email.policy import default
from django.db import models
from common.models import City, State, Country
from django.contrib.auth.models import User

# Create your models here.
class Vendor(models.Model):
    company_name = models.CharField(max_length=50, null=False)
    license_no = models.CharField(max_length=30, null=False)
    address_line1 = models.CharField(max_length=50, null=False)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=False)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='cities')
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    alternate_contact = models.CharField(max_length=10, null=False)
    phone_no = models.CharField(max_length=20, null=False)
    website = models.URLField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor_images')

    class Meta:
        verbose_name_plural = 'Vendor'