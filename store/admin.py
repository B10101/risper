# admin.py

from django.contrib import admin
from .models import Store

class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id', 'name', 'capacity', 'number_of_items', 'manager']
    list_filter = ['manager']
    search_fields = ['name', 'store_id']
    readonly_fields = ['store_id']

admin.site.register(Store, StoreAdmin)