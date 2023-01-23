from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'store_category', 'category']
    autocomplete_fields = ['category', 'vendor']
    search_fields = ['name']
    ordering = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark']
    search_fields = ['name']
    
