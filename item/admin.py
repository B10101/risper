# admin.py

from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'type', 'availability', 'reserved_by']
    list_filter = ['type', 'availability']
    search_fields = ['name', 'item_id', 'serial']
    readonly_fields = ['item_id']

admin.site.register(Item, ItemAdmin)