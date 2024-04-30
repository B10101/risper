from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved', 'is_admin']
    list_filter = ['is_approved', 'is_admin']
    actions = ['approve_users', 'reject_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    def reject_users(self, request, queryset):
        queryset.update(is_approved=False)
