from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Item
from django.db.models import Q
from store.models import Store



class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = "item/update_item.html"
    success_url = reverse_lazy('item:index')

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('item:index')

class ListAndCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        "name",
        "type",
        "serial",
        "cpu",
        "gpu",
        "ram",
    ]
    template_name = "item/create.html"
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        # Set the added_by field to the current user
        form.instance.added_by = self.request.user
        # Update the number of items in the associated store
        store = Store.objects.get(name=form.instance.item_store).number_of_items
        Store.objects.filter(name=form.instance.item_store).update(number_of_items=store + form.instance.item_num)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ListAndCreate, self).get_context_data(**kwargs)
        # Add the item list to the context
        context["item_list"] = self.model.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply search filter
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(type__icontains=search_query) |
                Q(serial__icontains=search_query)
            )
        return queryset

class ListAndDetail(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "item/item_list.html"

class ItemSearchView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item/search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(name__icontains=query) | Q(type__icontains=query) | Q(serial__icontains=query)
        )
        return object_list

class ItemReservationView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['return_date']
    template_name = "item/reserve_item.html"
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        form.instance.reserved_by = self.request.user
  # Set availability to False when item is reserved      
        form.instance.availability = False  
        return super().form_valid(form)

class AdminEquipmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Item
    template_name = "item/admin_equipment_list.html"
    context_object_name = 'equipment_list'

    def test_func(self):
        return self.request.user.is_staff  # Ensure only Admins can access this view
    

class AddEquipmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    template_name = "item/add_equipment.html"
    fields = '__all__'  # Include all fields from the Item model

    def test_func(self):
        return self.request.user.is_staff  # Ensure only Admins can access this view

class UpdateEquipmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = "item/update_equipment.html"
    fields = '__all__'  # Include all fields from the Item model

    def test_func(self):
        return self.request.user.is_staff  # Ensure only Admins can access this view
    

from django.views.generic import TemplateView

class InventoryReportView(LoginRequiredMixin, TemplateView):
    template_name = 'items/inventory_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve data for the inventory report
        context['total_items'] = Item.objects.count()
        context['available_items'] = Item.objects.filter(availability=True).count()
        context['unavailable_items'] = Item.objects.filter(availability=False).count()
        return context

class AddItemView(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        "name",
        "type",
        "serial",
        "cpu",
        "gpu",
        "ram",
    ]
    template_name = "items/add_item.html"
    success_url = reverse_lazy('items:inventory_report')  # Redirect to the inventory report after adding an item

from django.shortcuts import render
def home(request):
    template_name="item/homepage.html"
    return render(request, template_name)

class ItemCancelReservationView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = []  # No fields needed, as we're only canceling the reservation
    template_name = "item/cancel_reservation.html"  # Create this template for confirmation
    success_url = "/items/"  # Redirect to the item list page after cancellation

    def form_valid(self, form):
        # Set availability to True when reservation is canceled
        form.instance.availability = True
        # Clear the reserved_by field
        form.instance.reserved_by = None
        return super().form_valid(form)

class ItemReserveFromHistoryView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = []  # No fields needed, as we're only reserving the item
    template_name = "item/reserve_from_history.html"  # Create this template for confirmation
    success_url = "/items/"  # Redirect to the item list page after reservation

    def form_valid(self, form):
        # Set availability to False when item is reserved
        form.instance.availability = False
        # Set the current user as the one who reserved the item
        form.instance.reserved_by = self.request.user
        return super().form_valid(form)
from django import forms

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        "name",
        "type",
        "serial",
        "cpu",
        "gpu",
        "ram",
        "on_site_only",  # Include the new field in the form
    ]
    template_name = "item/create.html"
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = [
        "name",
        "type",
        "serial",
        "cpu",
        "gpu",
        "ram",
        "on_site_only",  # Include the new field in the form
    ]
    template_name = "item/update_item.html"
    success_url = reverse_lazy('item:index')
