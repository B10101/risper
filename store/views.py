from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
    ListView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mixins import AjaxableFormMixin
from store.models import Store
from item.models import Item
class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    fields = ['name', 'capacity', 'store_users']
    template_name = "store/create.html"
    success_url = reverse_lazy('store:create')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

# View for displaying store details
class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = "store/details.html"  # Template for displaying store details

class StoreDeleteView(LoginRequiredMixin, AjaxableFormMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('store:list')


class ItemReservationView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['return_date']  # Assuming return_date is the field used for reservation
    template_name = "item/reserve_item.html"  # Create this template to display the reservation form
    success_url = reverse_lazy('item:index')  # Redirect URL after successful reservation

    def form_valid(self, form):
        # Update the reserved_by field with the current user
        form.instance.reserved_by = self.request.user
        # Set availability to False when item is reserved
        form.instance.availability = False
        return super().form_valid(form)
class StoreListView(ListView):
    model = Store
    template_name = 'store/store_list.html'
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve reserved items
        reserved_items = Item.objects.filter(reserved_by__isnull=False)  # Filter items where reserved_by is not null
        context['reserved_items'] = reserved_items
        return context
