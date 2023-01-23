from django.contrib import admin
from . import models
from django.contrib import admin

# Register your models here.
@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'city_name', 'state']
    list_editable = ['city_name']
    autocomplete_fields = ['state']
    search_fields = ['city_name']

@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name', 'country']
    list_editable = ['state_name']
    autocomplete_fields = ['country']
    search_fields = ['state_name']

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'country_name']
    list_editable = ['country_name']
    search_fields = ['country_name']