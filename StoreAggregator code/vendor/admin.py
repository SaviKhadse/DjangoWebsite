from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'license_no', 'address_line1', 'address_line2', 'zipcode', 'city', 'state', 'country']
    search_fields = ['company_name']
    autocomplete_fields = ['city', 'state', 'country']
    ordering = ['id']